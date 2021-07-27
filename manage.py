from StockSituationRoom.crawl import *
from StockSituationRoom.model import Company, MonthRevenue
from StockSituationRoom import db
from datetime import date
import click
 
def init_company_db():
    grab_stock_name_tesk()

def init_revenue_db():
    today = date.today()
    last_year = today.year - 1
    this_month = today.month
    for month in range(1,13):
        revenue_to_db(year=last_year, month=month)
    for month in range(1,this_month):
        revenue_to_db(year=today.year,month=month)

@click.command()
@click.option('--init_db', 'init_db', help='initial database', 
                       type=str, required=True )
def init_db():
    init_company_db()
    init_revenue_db()

if __name__ == "__main__":
    init_db()
