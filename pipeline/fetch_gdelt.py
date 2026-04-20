"""
fetch_gdelt.py — Récupère les événements de conflit depuis GDELT
GDELT met à jour ses CSV toutes les 15 minutes, zéro clé requise.

Sortie : data/conflicts_raw.json
"""

import csv
import io
import json
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

import requests

# Dernier fichier GDELT Events 2.0 (mis à jour toutes les 15 min)
GDELT_LAST_UPDATE = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"

# Codes CAMEO = types d'événements retenus pour PaxIndex
# 14x = Protest, 15x = Coerce, 17x = Engage in unconventional mass violence,
# 18x = Attack, 19x = Use unconventional violence, 20x = Engage in mass killing
CONFLICT_CAMEO = {
    "14": "protest",
    "15": "coercition",
    "17": "violence_masse",
    "18": "attaque",
    "19": "violence_non_conv",
    "20": "massacre",
}

# Colonnes GDELT Events 2.0 (subset utilisé)
COLS = {
    "GLOBALEVENTID": 0,
    "DATEADDED": 1,
    "Actor1CountryCode": 7,
    "Actor2CountryCode": 17,
    "EventCode": 26,
    "GoldsteinScale": 30,   # -10 (conflictuel) à +10 (coopératif)
    "NumMentions": 31,
    "NumSources": 32,
    "AvgTone": 34,
    "Actor1Geo_CountryCode": 37,
    "ActionGeo_CountryCode": 51,
}

OUTPUT = Path(__file__).parent.parent / "data" / "conflicts_raw.json"


def get_latest_gdelt_url():
    """Récupère l'URL du dernier fichier CSV GDELT."""
    resp = requests.get(GDELT_LAST_UPDATE, timeout=10)
    resp.raise_for_status()
    # Format : "size url md5\nsize url md5\n..."
    lines = resp.text.strip().split("\n")
    # Première ligne = fichier export CSV
    for line in lines:
        parts = line.split(" ")
        if len(parts) >= 2 and parts[1].endswith("export.CSV.zip"):
            return parts[1]
    raise ValueError("URL GDELT introuvable dans lastupdate.txt")


def fetch_and_parse():
    print(f"[GDELT] Récupération du dernier fichier...")
    url = get_latest_gdelt_url()
    print(f"[GDELT] URL : {url}")

    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    conflicts = {}  # country_code → liste d'événements

    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        csv_name = z.namelist()[0]
        with z.open(csv_name) as f:
            reader = csv.reader(io.TextIOWrapper(f, encoding="utf-8"), delimiter="\t")
            for row in reader:
                if len(row) < 52:
                    continue

                event_code = row[COLS["EventCode"]]
                cameo_root = event_code[:2]
                if cameo_root not in CONFLICT_CAMEO:
                    continue

                goldstein = float(row[COLS["GoldsteinScale"]] or 0)
                if goldstein > -2:  # on garde seulement les events conflictuels
                    continue

                country = (
                    row[COLS["Actor1CountryCode"]] or
                    row[COLS["ActionGeo_CountryCode"]] or
                    ""
                ).strip().upper()

                if not country or len(country) != 3:
                    continue

                if country not in conflicts:
                    conflicts[country] = {
                        "country_code": country,
                        "event_count": 0,
                        "avg_goldstein": 0.0,
                        "avg_tone": 0.0,
                        "event_types": {},
                        "last_event": "",
                    }

                c = conflicts[country]
                n = c["event_count"]
                c["avg_goldstein"] = (c["avg_goldstein"] * n + goldstein) / (n + 1)
                tone = float(row[COLS["AvgTone"]] or 0)
                c["avg_tone"] = (c["avg_tone"] * n + tone) / (n + 1)
                c["event_count"] += 1
                c["last_event"] = row[COLS["DATEADDED"]]

                etype = CONFLICT_CAMEO[cameo_root]
                c["event_types"][etype] = c["event_types"].get(etype, 0) + 1

    result = {
        "source": "GDELT Events 2.0",
        "fetched_at": datetime.utcnow().isoformat(),
        "gdelt_url": url,
        "conflicts": list(conflicts.values()),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[GDELT] {len(conflicts)} pays avec événements conflictuels → {OUTPUT}")
    return result


if __name__ == "__main__":
    fetch_and_parse()
