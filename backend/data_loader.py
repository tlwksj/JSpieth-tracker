# Basic loading of data -- dummy data rn to build the bare bones.

import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "data", "spieth_scores.csv")

def load_data():
    df = pd.read_csv(file_path)
    df = df.sort_values("date")
    return df

def get_recent_scores(df, n=5):
    return df["score"].tail(n)