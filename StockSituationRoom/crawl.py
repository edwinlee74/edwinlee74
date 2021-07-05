import requests
import atexit
import csv
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from datetime import date
from StockSituationRoom.model import Company, MonthRevenue
from StockSituationRoom import db

stock_company_list_url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2' 
month_revenue_url = 'https://mops.twse.com.tw/nas/t21/sii/'

def get_html(url: str) -> str:
    try:
        headers = {'user-agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout = 30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return ""

def parse_company_list() -> list:
    html = get_html(stock_company_list_url)
    soup = BeautifulSoup(html, 'html.parser')
    index = 1        # An index of field value
    row_dict = {} 
    row_list = []

    for item in soup.find_all('td')[8:-1000]:    

         if not item.string: 
            index += 1
            continue

         if index == 8:
            row_list.append(row_dict)
            row_dict = {}
            index = 1
            stock = item.string
            stock_no = stock.split()[0]
            company = stock.split()[1]
            row_dict.update({'stock_no':stock_no})
            row_dict.update({'company_name':company})
         
         if index == 1:
            stock = item.string
            stock_no = stock.split()[0]
            company = stock.split()[1]
            row_dict.update({'stock_no':stock_no})
            row_dict.update({'company_name':company})

         if index == 3:
            date = item.string
            row_dict.update({'listing_date':date})
     
         if index == 5:
            category = item.string
            row_dict.update({'category':category})

         if item.string == '030001　萬海中信0B購01':
            row_list.append(row_dict)
            return row_list

         index += 1
 
def parse_company_revenue(year: str, month: str) -> list:
    row_list = []
    file = f't21sc03_{year}_{month}.csv'
    url = month_revenue_url + file
    csv_file = csv.reader(get_html(url).splitlines()[1:], delimiter=',')
    for item in csv_file:
       row_dict = {}
       stock_no = item[2]
       revenue = int(item[5])
       row_dict.update({'stock_no':stock_no,'revenue':revenue})
       row_list.append(row_dict)
    return row_list

def revenue_to_db(year: int, month: int) -> None:
    month_enum = {1:'january', 2:'february', 3:'march',
                  4:'april', 5:'may', 6:'june',
                  7:'july', 8:'august', 9:'september',
                  10:'october', 11:'november', 12:'december'}
    year_roc = year - 1911     #轉成民國年
    revenue_list = parse_company_revenue(year=str(year_roc), month=str(month))
    for revenue in revenue_list:
       result = MonthRevenue.query.filter(MonthRevenue.year==year_roc,
                           MonthRevenue.stock_no==revenue.get('stock_no')
                           ).first()                                       #檢查該筆記錄是否已存在
       if result:
          MonthRevenue.query.filter(MonthRevenue.year==year_roc,
                      MonthRevenue.stock_no==revenue.get('stock_no')).update(
                         {month_enum[month]:revenue.get('revenue')})
          db.session.commit()
       else:
          if month == 1:
             item = MonthRevenue(year=year_roc, january=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 2:
             item = MonthRevenue(year=year_roc, february=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 3:
             item = MonthRevenue(year=year_roc, march=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 4:
             item = MonthRevenue(year=year_roc, april=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 5:
             item = MonthRevenue(year=year_roc, may=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 6:
             item = MonthRevenue(year=year_roc, june=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 7:
             item = MonthRevenue(year=year_roc, july=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 8:
             item = MonthRevenue(year=year_roc, august=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 9:
             item = MonthRevenue(year=year_roc, september=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 10:
             item = MonthRevenue(year=year_roc, october=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 11:
             item = MonthRevenue(year=year_roc, november=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          if month == 12:
             item = MonthRevenue(year=year_roc, december=revenue.get('revenue'),
                       stock_no=revenue.get('stock_no'))
          db.session.add(item)
          db.session.commit()

def grab_stock_name_tesk():
    company_list = parse_company_list()
    Company.query.delete()
    db.session.commit()

    for company in company_list:
       item = Company(stock_no=company.get('stock_no'),
                      company_name=company.get('company_name'),
                      listing_date=company.get('listing_date'),
                      category=company.get('category')
               )
       db.session.add(item)
       db.session.commit()

def get_company_revenue_task():
    #parse_company_revenue()
    pass

scheduler = BackgroundScheduler()
scheduler.add_job(func=grab_stock_name_tesk, trigger='cron', minute='*/30')
scheduler.add_job(func=get_company_revenue_task, trigger='cron', minute='*/2')
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
