import pandas as pd

def predict_next_score(df):
    if df.empty:
        return None

    df = df.reset_index(drop=True)

    baseline = df["score"].mean()
    recent = df["score"].tail(3).mean()
    long_form = df["score"].tail(10).mean()

    momentum = recent - long_form

    prediction = (
        recent * 0.6 +
        baseline * 0.3 +
        momentum * 0.1
    )

    return round(prediction, 2)


def get_insights(df):
    insights = {}

    insights["avg_score"] = round(df["score"].mean(), 2)
    insights["best_score"] = df["score"].min()
    insights["worst_score"] = df["score"].max()

    recent = df["score"].tail(3).mean()
    long = df["score"].tail(10).mean()

    trend = recent - long

    if trend < 0:
        form = "Improving"
    elif trend > 0:
        form = "Declining"
    else:
        form = "Stable"

    insights["form_trend"] = form
    insights["trend_value"] = round(trend, 2)

    if "field_avg_score" in df.columns:
        df["difficulty_adjusted_score"] = df["score"] - df["field_avg_score"]

        insights["difficulty_adjusted_avg"] = round(
            df["difficulty_adjusted_score"].mean(), 2
        )

        insights["best_adjusted_performance"] = round(
            df["difficulty_adjusted_score"].min(), 2
        )
        
    return insights