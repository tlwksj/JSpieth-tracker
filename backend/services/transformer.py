import pandas as pd
from datetime import datetime

def transform_espn_data(data, target_player="Jordan Spieth"):
    rows = []

    events = data.get("events", [])

    for event in events:
        tournament = event.get("name", "Unknown Tournament")
        date = event.get("date", None)

        competitions = event.get("competitions", [])

        # field strength proxy (number of players)
        field_size = 0
        scores_for_difficulty = []

        for comp in competitions:
            competitors = comp.get("competitors", [])
            field_size = len(competitors)

            for c in competitors:
                try:
                    scores_for_difficulty.append(float(c.get("score", 0)))
                except:
                    continue

        field_avg = (
            sum(scores_for_difficulty) / len(scores_for_difficulty)
            if scores_for_difficulty else 0
        )

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
                    "date": date,
                    "score": score,
                    "vs_field": score - field_avg,

                    # NEW META FIELDS
                    "field_size": field_size,
                    "field_avg_score": field_avg,
                })

    return pd.DataFrame(rows)