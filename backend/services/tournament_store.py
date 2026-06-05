import pandas as pd
import os

TOURNAMENT_FILE = "data/tournaments.csv"

def init_tournament_file():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(TOURNAMENT_FILE):
        df = pd.DataFrame(columns=[
            "tournament_id",
            "tournament",
            "summary",
            "wiki_url",
            "field_size",
            "field_avg_score"
        ])
        df.to_csv(TOURNAMENT_FILE, index=False)


def load_tournaments():
    if not os.path.exists(TOURNAMENT_FILE):
        return pd.DataFrame()

    return pd.read_csv(TOURNAMENT_FILE)


def append_tournament(row):
    df = load_tournaments()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(TOURNAMENT_FILE, index=False)