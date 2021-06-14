from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config.from_file('config.json', load=json.load)
db = SQLAlchemy(app)

from StockSituationRoom import model
model.db.create_all()

from StockSituationRoom import route