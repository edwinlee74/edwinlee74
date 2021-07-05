from StockSituationRoom.crawl import *
from StockSituationRoom.model import Company, MonthRevenue
from StockSituationRoom import db

def init_revenue_db():
    revenue_to_db(year=2021, month=2)

init_revenue_db()

