# PaxIndex 🌍

**[🇫🇷 Français](#français) · [🇬🇧 English](#english)**

---

## English

### What is PaxIndex?

PaxIndex is an open-source web application that ranks countries based on their **degree of involvement in armed conflicts** and their **participation in international peace agreements and trade treaties**.

> **PaxIndex is not a well-being or quality-of-life index.**  
> It focuses solely on the geopolitical dimension: wars vs. agreements.

### How does it work?

Each country receives a **PaxScore™**, computed from two main signals:

| Signal | Source | Weight |
|--------|--------|--------|
| Armed conflict involvement | [GDELT Project](https://www.gdeltproject.org/) (updated every 15 min) | Negative |
| Peace & trade agreements | [Wikidata](https://www.wikidata.org/) | Positive |

A country with **few conflicts and many agreements** ranks at the top.  
A country **heavily involved in wars** ranks at the bottom.

### Features

- **World ranking** — countries sorted by PaxScore™
- **Interactive map** — geographic visualization
- **Country profiles** — conflicts, agreements, trade, trend over time
- **Alerts** — latest conflict events detected by GDELT
- **Trends** — score evolution over time
- **No API key required** — all data sources are free and open

### Tech stack

- Pure HTML/CSS/JS frontend (no framework)
- Python data pipeline (GDELT + Wikidata + RSS)
- Hosted on [Netlify](https://www.netlify.com/)
- CI/CD via GitHub Actions

### Status

> ⚠️ **Work in progress.** Data, scores, and features are actively being developed.

### Run locally

```bash
# Clone the repo
git clone https://github.com/XavierBonnel/paxindex.git
cd paxindex

# Open the app
open index.html

# Run the data pipeline (requires Python 3.10+)
cd pipeline
pip install -r requirements.txt
python run_pipeline.py
```

---

## Français

### Qu'est-ce que PaxIndex ?

PaxIndex est une application web open-source qui classe les pays selon leur **degré d'implication dans des conflits armés** et leur **participation à des accords de paix et traités commerciaux internationaux**.

> **PaxIndex n'est pas un indice de bien-être ou de qualité de vie.**  
> Il se concentre uniquement sur la dimension géopolitique : guerres versus accords.

### Comment ça fonctionne ?

Chaque pays reçoit un **PaxScore™**, calculé à partir de deux signaux principaux :

| Signal | Source | Effet |
|--------|--------|-------|
| Implication dans des conflits armés | [GDELT Project](https://www.gdeltproject.org/) (mis à jour toutes les 15 min) | Négatif |
| Accords de paix & traités commerciaux | [Wikidata](https://www.wikidata.org/) | Positif |

Un pays avec **peu de conflits et beaucoup d'accords** se retrouve en tête du classement.  
Un pays **fortement impliqué dans des guerres** se retrouve en bas.

### Fonctionnalités

- **Classement mondial** — pays triés par PaxScore™
- **Carte interactive** — visualisation géographique
- **Fiches pays** — conflits, accords, commerce, évolution dans le temps
- **Alertes** — derniers événements de conflit détectés par GDELT
- **Tendances** — évolution des scores dans le temps
- **Aucune clé API requise** — toutes les sources de données sont libres et ouvertes

### Stack technique

- Frontend HTML/CSS/JS pur (sans framework)
- Pipeline de données Python (GDELT + Wikidata + RSS)
- Hébergé sur [Netlify](https://www.netlify.com/)
- CI/CD via GitHub Actions

### Statut

> ⚠️ **Projet en cours de développement.** Les données, scores et fonctionnalités sont en cours de conception.

### Lancer en local

```bash
# Cloner le dépôt
git clone https://github.com/XavierBonnel/paxindex.git
cd paxindex

# Ouvrir l'application
open index.html

# Lancer le pipeline de données (Python 3.10+ requis)
cd pipeline
pip install -r requirements.txt
python run_pipeline.py
```

---

*Data sources: [GDELT Project](https://www.gdeltproject.org/) · [Wikidata](https://www.wikidata.org/)*
