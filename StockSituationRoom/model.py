from StockSituationRoom import db

class Company(db.Model):
    stock_no = db.Column(db.String(8), primary_key=True)
    company_name = db.Column(db.String(20))
    listing_date = db.Column(db.String(10))
    category = db.Column(db.String(30))
    
    def __repr__(self) -> str:
        return '<Company %r %r>' %(self.stock_no, self.company_name)
