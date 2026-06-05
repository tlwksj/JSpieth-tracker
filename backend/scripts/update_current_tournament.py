import json
from services.current_tournament import build_current_tournament

data = build_current_tournament()

with open("data/current_tournament.json", "w") as f:
    json.dump(data, f, indent=2)

print("Updated current tournament")