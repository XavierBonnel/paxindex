"""
compute_scores.py — Calcule le PaxScore™ pour chaque pays
à partir des données brutes GDELT + Wikidata.

Sortie : data/countries.json  (lu directement par l'app HTML via data.js)
         data/conflicts.json
         data/trade.json
         data/alerts.json
         data/stats.json
"""

import json
from datetime import datetime
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"

# ── Pays de référence avec leurs infos de base ──
# ISO 3166-1 alpha-3 → données statiques
COUNTRIES_BASE = {
    "ISL": {"code": "IS", "flag": "🇮🇸", "name": "Islande",          "region": "Europe",    "pop": 370_000},
    "DNK": {"code": "DK", "flag": "🇩🇰", "name": "Danemark",          "region": "Europe",    "pop": 5_900_000},
    "CHE": {"code": "CH", "flag": "🇨🇭", "name": "Suisse",            "region": "Europe",    "pop": 8_700_000},
    "NZL": {"code": "NZ", "flag": "🇳🇿", "name": "Nouvelle-Zélande",  "region": "Océanie",   "pop": 5_100_000},
    "SGP": {"code": "SG", "flag": "🇸🇬", "name": "Singapour",         "region": "Asie",      "pop": 5_900_000},
    "NOR": {"code": "NO", "flag": "🇳🇴", "name": "Norvège",           "region": "Europe",    "pop": 5_400_000},
    "SWE": {"code": "SE", "flag": "🇸🇪", "name": "Suède",             "region": "Europe",    "pop": 10_400_000},
    "FIN": {"code": "FI", "flag": "🇫🇮", "name": "Finlande",          "region": "Europe",    "pop": 5_500_000},
    "AUT": {"code": "AT", "flag": "🇦🇹", "name": "Autriche",          "region": "Europe",    "pop": 9_100_000},
    "PRT": {"code": "PT", "flag": "🇵🇹", "name": "Portugal",          "region": "Europe",    "pop": 10_300_000},
    "DEU": {"code": "DE", "flag": "🇩🇪", "name": "Allemagne",         "region": "Europe",    "pop": 83_800_000},
    "FRA": {"code": "FR", "flag": "🇫🇷", "name": "France",            "region": "Europe",    "pop": 68_300_000},
    "JPN": {"code": "JP", "flag": "🇯🇵", "name": "Japon",             "region": "Asie",      "pop": 124_000_000},
    "CAN": {"code": "CA", "flag": "🇨🇦", "name": "Canada",            "region": "Amériques", "pop": 38_300_000},
    "AUS": {"code": "AU", "flag": "🇦🇺", "name": "Australie",         "region": "Océanie",   "pop": 26_500_000},
    "BRA": {"code": "BR", "flag": "🇧🇷", "name": "Brésil",            "region": "Amériques", "pop": 215_000_000},
    "IND": {"code": "IN", "flag": "🇮🇳", "name": "Inde",              "region": "Asie",      "pop": 1_441_000_000},
    "CHN": {"code": "CN", "flag": "🇨🇳", "name": "Chine",             "region": "Asie",      "pop": 1_411_000_000},
    "GBR": {"code": "GB", "flag": "🇬🇧", "name": "Royaume-Uni",       "region": "Europe",    "pop": 67_700_000},
    "RUS": {"code": "RU", "flag": "🇷🇺", "name": "Russie",            "region": "Europe",    "pop": 144_000_000},
    "USA": {"code": "US", "flag": "🇺🇸", "name": "États-Unis",        "region": "Amériques", "pop": 335_000_000},
    "IRN": {"code": "IR", "flag": "🇮🇷", "name": "Iran",              "region": "Moyen-Orient","pop": 86_800_000},
    "ISR": {"code": "IL", "flag": "🇮🇱", "name": "Israël",            "region": "Moyen-Orient","pop": 9_700_000},
    "SAU": {"code": "SA", "flag": "🇸🇦", "name": "Arabie Saoudite",   "region": "Moyen-Orient","pop": 36_400_000},
    "ZAF": {"code": "ZA", "flag": "🇿🇦", "name": "Afrique du Sud",    "region": "Afrique",   "pop": 59_900_000},
    "NGA": {"code": "NG", "flag": "🇳🇬", "name": "Nigeria",           "region": "Afrique",   "pop": 223_000_000},
    "ETH": {"code": "ET", "flag": "🇪🇹", "name": "Éthiopie",          "region": "Afrique",   "pop": 126_000_000},
    "SDN": {"code": "SD", "flag": "🇸🇩", "name": "Soudan",            "region": "Afrique",   "pop": 46_900_000},
    "SYR": {"code": "SY", "flag": "🇸🇾", "name": "Syrie",             "region": "Moyen-Orient","pop": 22_100_000},
    "YEM": {"code": "YE", "flag": "🇾🇪", "name": "Yémen",             "region": "Moyen-Orient","pop": 34_500_000},
}

# Nombre d'accords commerciaux estimés (fallback si Wikidata indisponible)
TRADE_BASELINE = {
    "ISL": 68,  "DNK": 82,  "CHE": 110, "NZL": 76,  "SGP": 95,
    "NOR": 90,  "SWE": 88,  "FIN": 85,  "AUT": 84,  "PRT": 80,
    "DEU": 120, "FRA": 115, "JPN": 96,  "CAN": 88,  "AUS": 80,
    "BRA": 42,  "IND": 54,  "CHN": 130, "GBR": 62,  "RUS": 28,
    "USA": 214, "IRN": 15,  "ISR": 55,  "SAU": 35,  "ZAF": 48,
    "NGA": 30,  "ETH": 22,  "SDN": 8,   "SYR": 5,   "YEM": 4,
}

# Guerres historiques connues (fallback)
WARS_BASELINE = {
    "ISL": 0, "DNK": 0, "CHE": 0, "NZL": 1, "SGP": 0,
    "NOR": 0, "SWE": 0, "FIN": 1, "AUT": 0, "PRT": 2,
    "DEU": 2, "FRA": 6, "JPN": 1, "CAN": 2, "AUS": 3,
    "BRA": 2, "IND": 3, "CHN": 5, "GBR": 14,"RUS": 12,
    "USA": 42,"IRN": 8, "ISR": 7, "SAU": 5, "ZAF": 2,
    "NGA": 4, "ETH": 5, "SDN": 6, "SYR": 3, "YEM": 3,
}


def load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return None


def gdelt_conflict_score(gdelt_data, iso3):
    """Extrait le score de conflit GDELT pour un pays (alpha-3)."""
    if not gdelt_data:
        return 0.0
    for c in gdelt_data.get("conflicts", []):
        if c["country_code"] == iso3:
            # Goldstein : -10 (très conflictuel) → 0 (neutre)
            # On normalise sur 0-100 : score_brut = (goldstein + 10) / 10 * 100
            # Mais ici on veut un malus : plus c'est bas, plus le score paix baisse
            g = c["avg_goldstein"]  # négatif
            event_penalty = min(50, c["event_count"] * 0.5)
            return abs(g) * 5 + event_penalty
    return 0.0


def wikidata_trade_count(wiki_data, country_name):
    """Compte les accords commerciaux Wikidata pour un pays."""
    if not wiki_data:
        return None
    count = 0
    for agr in wiki_data.get("trade_agreements", []):
        if country_name in agr.get("countries", []):
            count += 1
    return count if count > 0 else None


def wikidata_conflict_count(wiki_data, country_name):
    """Compte les conflits Wikidata pour un pays."""
    if not wiki_data:
        return None
    count = 0
    for c in wiki_data.get("conflicts", []):
        if country_name in c.get("countries", []):
            count += 1
    return count if count > 0 else None


def compute_pax_score(wars, trade, gdelt_penalty=0):
    """
    PaxScore™ :
    - Paix (40%)     : basé sur guerres initiées + pénalité GDELT
    - Commerce (25%) : basé sur nb d'accords
    - Humanitaire (20%) : estimé depuis paix × 0.85
    - Diplomatie (15%)  : estimé depuis (paix + commerce) / 2
    """
    # Composante paix : 0-100
    paix = max(0, 100 - wars * 5 - gdelt_penalty)
    paix = min(100, paix)

    # Composante commerce : 0-100 (plafonné à 250 accords = 100)
    commerce = min(100, trade / 2.5)

    # Composantes estimées
    humanitaire = paix * 0.85
    diplomatie  = (paix + commerce) / 2

    score = (paix * 0.40 + commerce * 0.25 + humanitaire * 0.20 + diplomatie * 0.15)
    return round(score, 1)


def build_countries(gdelt_data, wiki_data):
    countries = []
    for iso3, base in COUNTRIES_BASE.items():
        wars  = wikidata_conflict_count(wiki_data, base["name"]) or WARS_BASELINE.get(iso3, 0)
        trade = wikidata_trade_count(wiki_data, base["name"])    or TRADE_BASELINE.get(iso3, 20)
        gdelt = gdelt_conflict_score(gdelt_data, iso3)

        score = compute_pax_score(wars, trade, gdelt)

        countries.append({
            "code":   base["code"],
            "flag":   base["flag"],
            "name":   base["name"],
            "region": base["region"],
            "score":  score,
            "change": 0.0,      # calculé sur 2 runs successifs
            "wars":   wars,
            "trade":  trade,
            "gdelt_penalty": round(gdelt, 1),
        })

    # Trier et assigner les rangs
    countries.sort(key=lambda c: c["score"], reverse=True)
    for i, c in enumerate(countries):
        c["rank"] = i + 1

    return countries


def build_conflicts(wiki_data):
    if not wiki_data:
        return []
    conflicts = []
    for c in wiki_data.get("conflicts", []):
        name = c["name"]
        countries_list = c.get("countries", [])
        # Mapper noms → drapeaux (approx)
        flags = []
        for cname in countries_list[:3]:
            match = next((b["flag"] for b in COUNTRIES_BASE.values() if b["name"] == cname), "🏳️")
            flags.append(match)
        conflicts.append({
            "id":        c["id"],
            "name":      name,
            "countries": flags,
            "type":      "guerre",
            "intensity": 70,  # À affiner avec GDELT Goldstein
            "since":     c.get("since") or "inconnue",
            "region":    "Inconnu",
        })
    return conflicts[:20]


def build_trade(wiki_data):
    if not wiki_data:
        return []
    result = []
    for agr in wiki_data.get("trade_agreements", [])[:30]:
        result.append({
            "id":        agr["id"],
            "name":      agr["name"],
            "countries": agr.get("countries", [])[:3],
            "type":      "bilateral" if len(agr.get("countries", [])) <= 2 else "regional",
            "status":    agr.get("status", "actif"),
            "signed":    agr.get("in_force") or "inconnu",
        })
    return result


def build_alerts(rss_data):
    if not rss_data:
        return []
    result = []
    for item in rss_data.get("alerts", [])[:20]:
        result.append({
            "id":      hash(item["title"]) % 10000,
            "level":   item["level"],
            "country": "🌍",
            "text":    item["title"][:80],
            "source":  item["source"],
            "link":    item.get("link", ""),
            "time":    item.get("published", "")[:16],
        })
    return result


def build_stats(countries):
    return {
        "totalCountries":   len(countries),
        "peacefulCount":    sum(1 for c in countries if c["wars"] == 0),
        "activeConflicts":  sum(c["wars"] for c in countries),
        "tradeAgreements":  sum(c["trade"] for c in countries) // 2,
        "generatedAt":      datetime.utcnow().isoformat(),
    }


def run():
    print("[Score] Chargement des données brutes...")
    gdelt = load_json(DATA / "conflicts_raw.json")
    wiki  = load_json(DATA / "trade_raw.json")
    rss   = load_json(DATA / "alerts_raw.json")

    print("[Score] Calcul des PaxScores...")
    countries = build_countries(gdelt, wiki)
    conflicts = build_conflicts(wiki)
    trade     = build_trade(wiki)
    alerts    = build_alerts(rss)
    stats     = build_stats(countries)

    # Écriture des JSON finaux (lus par l'app HTML)
    outputs = {
        "countries.json": countries,
        "conflicts.json": conflicts,
        "trade.json":     trade,
        "alerts.json":    alerts,
        "stats.json":     stats,
    }

    for fname, data in outputs.items():
        path = DATA / fname
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        count = len(data) if isinstance(data, list) else "ok"
        print(f"[Score] {fname} → {count}")

    print(f"\n✅ Pipeline terminé — {len(countries)} pays scorés")
    print(f"   Top 3 : {', '.join(c['name'] for c in countries[:3])}")
    print(f"   Bottom 3 : {', '.join(c['name'] for c in countries[-3:])}")


if __name__ == "__main__":
    run()
