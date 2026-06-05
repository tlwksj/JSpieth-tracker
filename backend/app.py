from flask import Flask, jsonify, render_template
from data_loader import load_data, get_recent_scores
from predictor import  predict_next_score, get_insights
from data_store import load_data
from scheduler import start_scheduler
from services.tournament_store import load_tournaments
from services.current_tournament import build_current_tournament

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

    prediction = predict_next_score(recent)

    return jsonify({
        "predicted_next_round_score": prediction
    })

@app.route("/dashboard")
def dashboard():
    df = load_data()
    tournaments = load_tournaments()
    current_tournament = build_current_tournament()
    tournament_map = {}
    if not tournaments.empty:
        tournament_map = tournaments.set_index("tournament_id").to_dict("index")


    prediction = predict_next_score(df, current_tournament.get("par"))
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
    recent=recent.to_dict("records"),
    chart_labels=chart_labels,
    chart_scores=chart_scores,
    chart_adjusted=chart_adjusted,
    current_tournament=current_tournament
)

if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True)