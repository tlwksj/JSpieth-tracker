import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_PATH = os.path.join(BASE_DIR, "data", "spieth_history.csv")

def init_file():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=[
            "player", "tournament", "score", "vs_field"
        ])
        df.to_csv(FILE_PATH, index=False)

def append_data(df_new):
    if os.path.exists(FILE_PATH):
        df_old = pd.read_csv(FILE_PATH)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(FILE_PATH, index=False)

def load_data():
    return pd.read_csv(FILE_PATH)