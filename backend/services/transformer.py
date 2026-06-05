import pandas as pd
from datetime import datetime
from services.wiki import get_tournament_info
from services.tournament_store import append_tournament, load_tournaments
import hashlib

def make_tournament_id(name):
    return hashlib.md5(name.encode()).hexdigest()


def transform_espn_data(data, target_player="Jordan Spieth"):
    rows = []
    tournaments_seen = set()

    events = data.get("events", [])

    for event in events:
        tournament = event.get("name", "Unknown Tournament")
        tournament_id = make_tournament_id(tournament)

        competitions = event.get("competitions", [])

        field_scores = []
        field_size = 0

        for comp in competitions:
            competitors = comp.get("competitors", [])
            field_size = len(competitors)

            for c in competitors:
                try:
                    field_scores.append(float(c.get("score", 0)))
                except:
                    pass

        field_avg = (
            sum(field_scores) / len(field_scores)
            if field_scores else 0
        )

        # ---- TOURNAMENT TABLE (ONLY ONCE PER TOURNAMENT)
        if tournament_id not in tournaments_seen:
            wiki = get_tournament_info(tournament)

            tournament_row = {
                "tournament_id": tournament_id,
                "tournament": tournament,
                "summary": wiki["summary"],
                "wiki_url": wiki["url"],
                "field_size": field_size,
                "field_avg_score": field_avg
            }

            append_tournament(tournament_row)
            tournaments_seen.add(tournament_id)

        # ---- PLAYER ROWS
        for comp in competitions:
            competitors = comp.get("competitors", [])

            for c in competitors:
                athlete = c.get("athlete", {})
                player = athlete.get("displayName", "")

                if target_player.lower() not in player.lower():
                    continue

                try:
                    score = float(c.get("score", 0))
                except:
                    continue

                rows.append({
                    "player": player,
                    "tournament": tournament,
                    "tournament_id": tournament_id,
                    "score": score,
                    "vs_field": score - field_avg
                })

    return pd.DataFrame(rows)