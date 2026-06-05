from flask import Flask, jsonify, render_template
from data_loader import load_data, get_recent_scores
from predictor import  predict_next_score, get_insights
from data_store import load_data
from scheduler import start_scheduler

app = Flask(__name__)
@app.route("/")
def home():
    return "Spieth Tracker API is running"

@app.route("/stats")
def stats():
    df = load_data()

    return jsonify({
        "recent_scores": df["score"].tail(10).tolist(),
        "season_avg": float(df["score"].mean())
    })

@app.route("/predict")
def predict():
    df = load_data()
    recent = get_recent_scores(df)

    prediction = predict_next_round(recent)

    return jsonify({
        "predicted_next_round_score": prediction
    })

@app.route("/dashboard")
def dashboard():
    df = load_data()

    prediction = predict_next_score(df)
    insights = get_insights(df)

    # IMPORTANT: make sure data is in order
    if "date" in df.columns:
        df = df.sort_values("date")

    recent = df.tail(10)

    chart_labels = recent["tournament"].tolist()
    chart_scores = recent["score"].tolist()
    chart_adjusted = recent["vs_field"].tolist()

    return render_template(
        "dashboard.html",
        prediction=prediction,
        insights=insights,
        recent=recent.to_dict(orient="records"),
        chart_labels=chart_labels,
        chart_scores=chart_scores,
        chart_adjusted=chart_adjusted
    )

if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True)