"""
fetch_wikidata.py — Récupère les accords commerciaux actifs depuis Wikidata
API REST Wikidata, gratuit, sans clé.

Sortie : data/trade_raw.json
"""

import json
from datetime import datetime
from pathlib import Path

import requests

OUTPUT = Path(__file__).parent.parent / "data" / "trade_raw.json"

# SPARQL endpoint Wikidata
SPARQL_URL = "https://query.wikidata.org/sparql"

HEADERS = {
    "User-Agent": "PaxIndex/1.0 (contact: paxindex@proton.me)",
    "Accept": "application/sparql-results+json",
}

# Requête SPARQL : accords commerciaux (Q15243209 = trade agreement)
QUERY_TRADE = """
SELECT DISTINCT ?agreement ?agreementLabel ?country1 ?country1Label ?country2 ?country2Label ?inForce WHERE {
  ?agreement wdt:P31/wdt:P279* wd:Q15243209 .
  ?agreement wdt:P1001 ?country1 .
  OPTIONAL { ?agreement wdt:P1001 ?country2 . FILTER(?country2 != ?country1) }
  OPTIONAL { ?agreement wdt:P7588 ?inForce }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
}
LIMIT 500
"""

# Requête SPARQL : conflits armés en cours (Q180684 = armed conflict)
QUERY_CONFLICTS = """
SELECT DISTINCT ?conflict ?conflictLabel ?country ?countryLabel ?start WHERE {
  ?conflict wdt:P31/wdt:P279* wd:Q180684 .
  ?conflict wdt:P17 ?country .
  OPTIONAL { ?conflict wdt:P580 ?start }
  FILTER NOT EXISTS { ?conflict wdt:P582 ?end }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr,en". }
}
LIMIT 200
"""


def run_sparql(query, label):
    print(f"[Wikidata] Requête {label}...")
    try:
        resp = requests.get(
            SPARQL_URL,
            params={"query": query, "format": "json"},
            headers=HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["results"]["bindings"]
    except Exception as e:
        print(f"[Wikidata] Erreur {label}: {e}")
        return []


def parse_trade(bindings):
    agreements = {}
    for row in bindings:
        uri = row.get("agreement", {}).get("value", "")
        qid = uri.split("/")[-1]
        name = row.get("agreementLabel", {}).get("value", qid)
        c1 = row.get("country1Label", {}).get("value", "")
        c2 = row.get("country2Label", {}).get("value", "")
        in_force = row.get("inForce", {}).get("value", "")

        if qid not in agreements:
            agreements[qid] = {
                "id": qid,
                "name": name,
                "countries": [],
                "in_force": in_force[:10] if in_force else None,
                "status": "actif" if in_force else "inconnu",
            }
        for c in [c1, c2]:
            if c and c not in agreements[qid]["countries"]:
                agreements[qid]["countries"].append(c)

    return list(agreements.values())


def parse_conflicts(bindings):
    conflicts = {}
    for row in bindings:
        uri = row.get("conflict", {}).get("value", "")
        qid = uri.split("/")[-1]
        name = row.get("conflictLabel", {}).get("value", qid)
        country = row.get("countryLabel", {}).get("value", "")
        start = row.get("start", {}).get("value", "")

        if qid not in conflicts:
            conflicts[qid] = {
                "id": qid,
                "name": name,
                "countries": [],
                "since": start[:10] if start else None,
                "type": "guerre",
            }
        if country and country not in conflicts[qid]["countries"]:
            conflicts[qid]["countries"].append(country)

    return list(conflicts.values())


def fetch_all():
    trade_raw    = run_sparql(QUERY_TRADE, "accords commerciaux")
    conflict_raw = run_sparql(QUERY_CONFLICTS, "conflits armés")

    trade_data    = parse_trade(trade_raw)
    conflict_data = parse_conflicts(conflict_raw)

    result = {
        "source": "Wikidata SPARQL",
        "fetched_at": datetime.utcnow().isoformat(),
        "trade_agreements": trade_data,
        "conflicts": conflict_data,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[Wikidata] {len(trade_data)} accords · {len(conflict_data)} conflits → {OUTPUT}")
    return result


if __name__ == "__main__":
    fetch_all()
