import requests

ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/golf/pga/scoreboard"

def fetch_live_tournaments():
    response = requests.get(ESPN_URL)
    data = response.json()
    return data


def extract_player_scores(data, player_name="Jordan Spieth"):
    results = []

    events = data.get("events", [])

    for event in events:
        competitions = event.get("competitions", [])

        for comp in competitions:
            competitors = comp.get("competitors", [])

            for c in competitors:
                athlete = c.get("athlete", {}).get("displayName", "")

                if player_name.lower() in athlete.lower():
                    results.append({
                        "player": athlete,
                        "score": c.get("score"),
                        "status": c.get("status", {}).get("displayValue")
                    })

    return c