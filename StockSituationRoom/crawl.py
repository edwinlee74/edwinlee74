from apscheduler.schedulers.background import BackgroundScheduler

def crawl_tesk():
    print("crawl tesk begin...")

def tesk2():
    print("tesk2 starting...")

scheduler = BackgroundScheduler()
scheduler.add_job(func=crawl_tesk, trigger='cron', minute='*/1', max_instances=3)
scheduler.start()

scheduler2 = BackgroundScheduler()
scheduler2.add_job(func=tesk2, trigger='cron', minute='*/2')
scheduler2.start()
