from apscheduler.schedulers.background import BackgroundScheduler
from .services.espn_api import fetch_live_tournaments
from .services.transformer import transform_espn_data
from .data_store import init_file, append_data

def update_pipeline():
    print("Running scheduled update...")

    data = fetch_live_tournaments()
    df = transform_espn_data(data)

    if not df.empty:
        append_data(df)

    print("Update complete")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_pipeline, "interval", minutes=10)
    scheduler.start()

    print("Scheduler started (runs every 10 minutes)")