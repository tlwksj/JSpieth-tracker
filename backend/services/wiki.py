import wikipedia
import requests
from bs4 import BeautifulSoup

_cache = {}


def get_wikipedia_infobox(url):
    try:
        if not url:
            return {}

        url = url.split("#")[0]

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(url, headers=headers, timeout=10)

        if res.status_code != 200:
            print("Infobox HTTP error:", res.status_code)
            return {}

        soup = BeautifulSoup(res.text, "lxml")

        infobox = soup.find("table", class_=lambda x: x and "infobox" in x)

        if not infobox:
            return {}

        data = {}

        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")

            if th and td:
                key = th.get_text(" ", strip=True)
                val = td.get_text(" ", strip=True)
                data[key] = val

        return data

    except Exception as e:
        print("Wiki infobox error:", e)
        return {}

def normalize_tournament(name):
    name = name.lower()

    removals = [
        "pres. by workday",
        "presented by",
        "the "
    ]

    for r in removals:
        name = name.replace(r, "")

    return " ".join(name.split()).strip()



def get_tournament_info(name):
    base = {
        "title": None,
        "url": None,
        "summary": None,

        "location": None,
        "course": None,
        "par": None,
        "yardage": None,
        "tour": None,
        "format": None,
        "prize_fund": None,
        "month_played": None,
        "aggregate": None,
        "to_par": None
    }

    try:
        results = wikipedia.search(normalize_tournament(name))

        if not results:
            return base

        page_title = results[0]

        page = None

    
        try:
            page = wikipedia.page(page_title)
            base["title"] = page.title
            base["url"] = page.url
        except Exception as e:
            print("Wikipedia page error:", e)

        try:
            base["summary"] = wikipedia.summary(page_title, sentences=2)
        except Exception as e:
            print("Wikipedia summary error:", e)

        try:
            if page:
                infobox = get_wikipedia_infobox(page.url)

                base["location"] = infobox.get("Location")
                base["course"] = infobox.get("Course")
                base["par"] = infobox.get("Par")

                base["yardage"] = infobox.get("Yardage") or infobox.get("Length")

                base["tour"] = infobox.get("Tour")
                base["format"] = infobox.get("Format")
                base["prize_fund"] = infobox.get("Prize fund")

                base["month_played"] = infobox.get("Month played")
                base["aggregate"] = infobox.get("Aggregate")
                base["to_par"] = infobox.get("To par")

        except Exception as e:
            print("Infobox merge error:", e)

        return base

    except Exception as e:
        print("Wiki pipeline error:", e)
        return base