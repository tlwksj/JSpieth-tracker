import pandas as pd

def transform_espn_data(data, target_player="Jordan Spieth"):
    rows = []

    events = data.get("events", [])

    for event in events:
        tournament = event.get("name", "Unknown Tournament")

        competitions = event.get("competitions", [])

        for comp in competitions:
            competitors = comp.get("competitors", [])

            # compute field average (still useful for context)
            scores = []

            for c in competitors:
                try:
                    scores.append(float(c.get("score", 0)))
                except:
                    continue

            field_avg = sum(scores) / len(scores) if scores else 0

            # ONLY extract Spieth
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
                    "score": score,
                    "vs_field": score - field_avg
                })

    return pd.DataFrame(rows)