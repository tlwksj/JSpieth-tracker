import requests
import hashlib
from .wiki import get_tournament_info


def fetch_current_tournament():
    url = "https://site.api.espn.com/apis/site/v2/sports/golf/pga/scoreboard"
    res = requests.get(url)
    data = res.json()

    events = data.get("events", [])

    if not events:
        return None

    event = events[0]

    return {
        "name": event.get("name"),
        "date": event.get("date"),
        "id": event.get("id")
    }


def make_tournament_id(name):
    return hashlib.md5(name.lower().encode()).hexdigest()


def build_current_tournament():
    event = fetch_current_tournament()

    if not event:
        return None

    wiki = get_tournament_info(event["name"]) or {}

    return {
        "tournament_id": make_tournament_id(event["name"]),
        "name": event["name"],

        "summary": wiki.get("summary"),
        "wiki_url": wiki.get("url"),

        "location": wiki.get("location"),
        "course": wiki.get("course"),
        "par": wiki.get("par"),
        "yardage": wiki.get("yardage"),

        "last_winner": wiki.get("aggregate"),  # or replace later properly
        "last_score": wiki.get("to_par")
    }