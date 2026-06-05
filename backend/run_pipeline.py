from services.espn_api import fetch_live_tournaments
from services.transformer import transform_espn_data
from services import spieth_is_playing
from data_store import init_file, append_data, load_data
from predictor import predict_next_score, get_insights
import sys

init_file()

data = fetch_live_tournaments()

if not spieth_is_playing(data):
    print("Spieth not playing. Exiting pipeline.")
    sys.exit(0)

df_new = transform_espn_data(data)
append_data(df_new)

df = load_data()

prediction = predict_next_score(df)
insights = get_insights(df)

print("Prediction:", prediction)
print("Insights:", insights)