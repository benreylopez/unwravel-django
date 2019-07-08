from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from portal import views
import os
from django.conf import settings

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(views.portal_scrape, 'interval', minutes=1)
	scheduler.start()