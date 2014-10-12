from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hackpr@104.131.99.25:3306/hackpratru'
db = SQLAlchemy(app)

class Invoice(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    from_ = db.Column('from', db.String)
    status = db.relationship('Status', backref=db.backref('invoices', lazy='dynamic'))
    invoice_num = db.Column('invoiceNum', db.String)
    created = db.Column(db.DateTime)
    status_id = db.Column('status', db.Integer, db.ForeignKey('status.id'))

    def __init__(self, from_, invoice_num, status_id=1):
        self.from_ = from_
        self.invoice_num = invoice_num
        self.status_id=status_id


    def __repr__(self):
        return 'From: ' + self.from_ + ', Invoice Number: ' + self.invoice_num + ', Status: ' + str(self.status)

class Establishment(db.Model):
    __tablename__ = 'establishment'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    created_ts = db.Column(db.DateTime)

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __repr__(self):
        return 'Name: ' + self.name + ', Phone: ' + self.phone

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Float)

    store_id = db.Column('store',db.Integer, db.ForeignKey('establishment.id'))
    store = db.relationship('Establishment', backref=db.backref('items', lazy='dynamic'))

    def __init__(self, name, description, price, store):
        self.name = name
        self.description = description
        self.price = price
        self.store = store

    def __repr__(self):
        return 'Name: ' + self.name + ", Descrption: " + self.description + ', Price: ' + str(self.price) + ', Store: ' + str(self.store)

class Order(db.Model):
    __tablename__ = 'order'
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'),primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'),primary_key=True)

    def __init__(self, invoice_id, item_id):
        self.invoice_id = invoice_id
        self.item_id = item_id

    def __repr__(self):
        return 'Invoice ID: ' + str(self.invoice_id) + ', Item ID: ' + str(self.item_id)

class Status(db.Model):
    __status__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Name: ' + self.name

#print(str(Invoice.query.all()))

#print(str(Establishment.query.all()))

#print(str(Item.query.all()))

#print(str(Order.query.all()))

#print(str(Status.query.all()))