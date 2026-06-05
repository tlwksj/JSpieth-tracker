def spieth_is_playing(data):
    events = data.get("events", [])

    for event in events:
        competitions = event.get("competitions", [])

        for comp in competitions:
            competitors = comp.get("competitors", [])

            for c in competitors:
                athlete = c.get("athlete", {})
                name = athlete.get("displayName", "")

                if "spieth" in name.lower():
                    return True

    return False