from flask import render_template, request
from StockSituationRoom import app
from StockSituationRoom.model import Company, MonthRevenue
from StockSituationRoom import db
from datetime import date

@app.get("/")
def index():
    return render_template('index.html')

@app.get("/api/data")
def data():
    query = Company.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Company.stock_no.like(f'%{search}%'),
            Company.company_name.like(f'%{search}%'),
            Company.category.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['stock_no', 'company_name', 'listing_date','category']:
            col_name = 'stock_no'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Company, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    
    if order:
        query = query.order_by(*order)
    
    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length',type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [company.to_dict() for company in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Company.query.count(),
        'draw': request.args.get('draw',type=int)
        }

@app.get("/api/revenue/<stock_no>")
def revenue(stock_no: str) -> dict:
    today = date.today()
    thisYear = today.year - 1911
    lastYear = thisYear - 1
    thisYearRevenue = MonthRevenue.query.filter(
                                             MonthRevenue.year == thisYear,
                                             MonthRevenue.stock_no == stock_no
                                    ).first()
    lastYearRevenue = MonthRevenue.query.filter(
                                               MonthRevenue.year == lastYear,
                                               MonthRevenue.stock_no == stock_no
                                    ).first()
    
    thisYearRevenueList = [thisYearRevenue.january, thisYearRevenue.february,
                                         thisYearRevenue.march, thisYearRevenue.april,
                                         thisYearRevenue.may, thisYearRevenue.june,
                                         thisYearRevenue.july, thisYearRevenue.august,
                                         thisYearRevenue.september, thisYearRevenue.october,
                                         thisYearRevenue.november, thisYearRevenue.december]

    lastYearRevenueList = [lastYearRevenue.january, lastYearRevenue.february,
                                         lastYearRevenue.march, lastYearRevenue.april,
                                         lastYearRevenue.may, lastYearRevenue.june,
                                         lastYearRevenue.july, lastYearRevenue.august,
                                         lastYearRevenue.september, lastYearRevenue.october,
                                         lastYearRevenue.november, lastYearRevenue.december]

    return {
        'thisYear': thisYearRevenueList,
        'lastYear': lastYearRevenueList
    }