from flask import render_template
from StockSituationRoom import app

@app.get("/")
def hello_world():
    return render_template('base.html')