"""
fetch_rss.py — Récupère et résume les alertes géopolitiques depuis des flux RSS gratuits
Aucune clé API requise.

Sortie : data/alerts_raw.json
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import requests

OUTPUT = Path(__file__).parent.parent / "data" / "alerts_raw.json"

FEEDS = [
    {
        "name": "International Crisis Group",
        "url": "https://www.crisisgroup.org/rss-0",
        "category": "conflit",
    },
    {
        "name": "RAND Corporation",
        "url": "https://www.rand.org/news/rss.xml",
        "category": "géopolitique",
    },
    {
        "name": "Chatham House",
        "url": "https://www.chathamhouse.org/rss/research-publications",
        "category": "diplomatie",
    },
    {
        "name": "Global Voices",
        "url": "https://globalvoices.org/feed/",
        "category": "terrain",
    },
    {
        "name": "ReliefWeb — Conflits",
        "url": "https://reliefweb.int/updates/rss.xml?primary_country=0&source=0&type=news&theme=crisis",
        "category": "humanitaire",
    },
    {
        "name": "Al Jazeera English",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "category": "actualité",
    },
    {
        "name": "France 24 Monde",
        "url": "https://www.france24.com/fr/rss",
        "category": "actualité",
    },
]

HEADERS = {"User-Agent": "PaxIndex/1.0 (aggregateur public)"}

# Mots-clés pour scorer la criticité
CRITICAL_WORDS = ["war", "strike", "attack", "bomb", "killed", "dead", "conflict",
                  "guerre", "frappe", "attentat", "tués", "mort", "conflit", "invasion"]
HIGH_WORDS     = ["tension", "sanction", "ceasefire", "troops", "military",
                  "armée", "soldats", "embargo", "missiles", "explosion"]


def score_item(title, summary):
    text = (title + " " + summary).lower()
    if any(w in text for w in CRITICAL_WORDS):
        return "critical"
    if any(w in text for w in HIGH_WORDS):
        return "high"
    return "medium"


def parse_feed(feed_cfg):
    items = []
    try:
        resp = requests.get(feed_cfg["url"], headers=HEADERS, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)

        # Support RSS 2.0 et Atom
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall(".//item") or root.findall(".//atom:entry", ns)

        for entry in entries[:10]:  # 10 derniers items par flux
            title   = (entry.findtext("title") or
                       entry.findtext("atom:title", namespaces=ns) or "").strip()
            link    = (entry.findtext("link") or
                       entry.findtext("atom:link", namespaces=ns) or "")
            summary = (entry.findtext("description") or
                       entry.findtext("atom:summary", namespaces=ns) or "").strip()
            pub_date= (entry.findtext("pubDate") or
                       entry.findtext("atom:published", namespaces=ns) or "")

            # Nettoyer le HTML basique du summary
            import re
            summary_clean = re.sub(r"<[^>]+>", "", summary)[:200]

            if title:
                items.append({
                    "title": title,
                    "summary": summary_clean,
                    "link": link,
                    "published": pub_date,
                    "source": feed_cfg["name"],
                    "category": feed_cfg["category"],
                    "level": score_item(title, summary_clean),
                })

        print(f"[RSS] {feed_cfg['name']} → {len(items)} items")
    except Exception as e:
        print(f"[RSS] Erreur {feed_cfg['name']}: {e}")

    return items


def fetch_all():
    all_items = []
    for feed in FEEDS:
        all_items.extend(parse_feed(feed))

    # Trier par criticité
    order = {"critical": 0, "high": 1, "medium": 2}
    all_items.sort(key=lambda x: order.get(x["level"], 3))

    result = {
        "source": "RSS aggregation",
        "fetched_at": datetime.utcnow().isoformat(),
        "feeds_count": len(FEEDS),
        "items_count": len(all_items),
        "alerts": all_items,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[RSS] {len(all_items)} alertes totales → {OUTPUT}")
    return result


if __name__ == "__main__":
    fetch_all()
