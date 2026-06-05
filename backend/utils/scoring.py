def to_actual_score(predicted_to_par, par):
    if predicted_to_par is None or par is None:
        return None
    return round(int(par) + predicted_to_par, 2)