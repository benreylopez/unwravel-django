from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from portfolio import views

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(views.products_scrape, 'interval', minutes=1440)
    scheduler.start()