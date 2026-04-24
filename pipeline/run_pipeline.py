
import argparse
import sys
import time
from datetime import datetime

# ── import des modules du pipeline ──
try:
    from fetch_gdelt    import fetch_and_parse as fetch_gdelt
    from fetch_wikidata import fetch_all       as fetch_wikidata
    from fetch_rss      import fetch_all       as fetch_rss
    from compute_scores import run             as compute_scores
except ImportError:
    import importlib, os
    sys.path.insert(0, os.path.dirname(__file__))
    from fetch_gdelt    import fetch_and_parse as fetch_gdelt
    from fetch_wikidata import fetch_all       as fetch_wikidata
    from fetch_rss      import fetch_all       as fetch_rss
    from compute_scores import run             as compute_scores


def banner(msg):
    print(f"\n{'─'*50}")
    print(f"  {msg}")
    print(f"{'─'*50}")


def run(args):
    start = time.time()
    print(f"\n🚀 PaxIndex Pipeline — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    errors = []

    if not args.scores_only:
        # 1. GDELT (événements conflits 15 min)
        if not args.rss_only:
            banner("1/3 GDELT — Événements conflictuels")
            try:
                fetch_gdelt()
            except Exception as e:
                print(f"⚠️  GDELT échoué : {e} — on continue avec les données existantes")
                errors.append(f"GDELT: {e}")

        # 2. Wikidata (accords + conflits structurés)
        if not args.rss_only:
            banner("2/3 Wikidata — Accords & conflits")
            try:
                fetch_wikidata()
            except Exception as e:
                print(f"⚠️  Wikidata échoué : {e} — on continue")
                errors.append(f"Wikidata: {e}")

        # 3. RSS (alertes temps réel)
        banner("3/3 RSS — Alertes géopolitiques")
        try:
            fetch_rss()
        except Exception as e:
            print(f"⚠️  RSS échoué : {e}")
            errors.append(f"RSS: {e}")

    # 4. Calcul des scores
    banner("4/4 Calcul des PaxScores™")
    try:
        compute_scores()
    except Exception as e:
        print(f"❌  Calcul des scores échoué : {e}")
        errors.append(f"Scores: {e}")
        sys.exit(1)

    elapsed = round(time.time() - start, 1)
    print(f"\n✅ Pipeline terminé en {elapsed}s")

    if errors:
        print(f"⚠️  {len(errors)} avertissement(s) :")
        for err in errors:
            print(f"   • {err}")

    print("📁 Fichiers mis à jour dans data/")
    print("   countries.json · trade.json · alerts.json · stats.json\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de données PaxIndex")
    parser.add_argument("--scores-only", action="store_true",
                        help="Recalculer les scores sans re-fetcher les sources")
    parser.add_argument("--rss-only", action="store_true",
                        help="Mettre à jour uniquement les alertes RSS")
    args = parser.parse_args()
    run(args)
