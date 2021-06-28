import requests
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
from datetime import date

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

def parse_company_list():
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
 
def parse_company_revenue():
    today = date.today()
    year = str(today.year - 1911)              #轉成民國年號
    month = str(today.month)
    file = f't21sc03_{year}_{month}.csv'
    url = month_revenue_url + file
    csv_file = get_html(url)
    for item in csv_file.splitlines()[1:]:
       stock_no = item.split(',')[2]
       revenue = item.split(',')[5]
       print(stock_no, ' ', revenue)

def grab_stock_name_tesk():
    company_list = parse_company_list()
    print(company_list)
    return

def get_company_revenue_task():
    parse_company_revenue()

scheduler = BackgroundScheduler()
scheduler.add_job(func=grab_stock_name_tesk, trigger='cron', minute='*/30')
scheduler.add_job(func=get_company_revenue_task, trigger='cron', minute='*/2')
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
