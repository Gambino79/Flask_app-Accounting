from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(115))
    amount_expense = db.Column(db.Integer)
    date_paid = db.Column(db.Date())
    date_month_ex = db.Column(db.String(20))
    switch_paid = db.Column(db.String(1))

class Revenues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(115))
    amount_revenue = db.Column(db.Integer)
    date_received = db.Column(db.Date())
    date_month_re = db.Column(db.String(20))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))