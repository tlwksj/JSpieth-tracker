from flask import Flask, jsonify, render_template
from data_loader import load_data, get_recent_scores
from predictor import predict_next_round

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
    recent = df["score"].tail(10).tolist()
    prediction = predict_next_round(df["score"])

    return render_template(
        "dashboard.html",
        recent_scores=recent,
        prediction=prediction
    )

if __name__ == "__main__":
    app.run(debug=True)