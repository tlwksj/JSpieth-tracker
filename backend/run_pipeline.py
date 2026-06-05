if __name__ == "__main__":
    from services.espn_api import fetch_live_tournaments
    from services.transformer import transform_espn_data
    from data_store import init_file, append_data, load_data
    from predictor import predict_next_score, get_insights

    init_file()

    data = fetch_live_tournaments()

    df_new = transform_espn_data(data)
    append_data(df_new)

    df = load_data()

    prediction = predict_next_score(df)
    insights = get_insights(df)

    print("Prediction:", prediction)
    print("Insights:", insights)