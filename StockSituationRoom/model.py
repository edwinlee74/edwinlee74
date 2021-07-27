from StockSituationRoom import db

class Company(db.Model):
    stock_no = db.Column(db.String(8), primary_key=True)
    company_name = db.Column(db.String(20))
    listing_date = db.Column(db.String(10))
    category = db.Column(db.String(30))
    
    def to_dict(self) -> dict:
        return {
            'stock_no': self.stock_no,
            'company_name': self.company_name,
            'listing_date': self.listing_date,
            'category': self.category
        }

    def __repr__(self) -> str:
        return '<Company %r %r>' %(self.stock_no, self.company_name)

class MonthRevenue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    january = db.Column(db.Integer)
    february = db.Column(db.Integer)
    march = db.Column(db.Integer)
    april = db.Column(db.Integer)
    may = db.Column(db.Integer)
    june = db.Column(db.Integer)
    july = db.Column(db.Integer)
    august = db.Column(db.Integer)
    september = db.Column(db.Integer)
    october = db.Column(db.Integer)
    november = db.Column(db.Integer)
    december = db.Column(db.Integer)
    stock_no = db.Column(db.String(8), db.ForeignKey('company.stock_no'))

    def __repr__(self) -> str:
        return '<MonthRevenue %r>' % self.stock_no