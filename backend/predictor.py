# Basic predictor (Not actually ML)

import numpy as np

def predict_next_round(scores):
    scores = list(scores)

    last_5_avg = np.mean(scores[-5:])
    season_avg = np.mean(scores)

    prediction = 0.6 * last_5_avg + 0.4 * season_avg

    return round(prediction, 2)