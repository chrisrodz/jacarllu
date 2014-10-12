import orm

class Dao:

    def __init__(self):
        return

    def getInvoices(self, from_):
        results = orm.Invoice.query.filter_by(from_=from_).all();
        return results
    def updateInvoice(self, invoiceNum, status):
        result = orm.Invoice.query.filter_by(invoice_num=invoiceNum).first()
        result.status = status
        orm.db.session.commit()
        return result
    def addInvoice(self, from_, invoice_num):
        invoice = orm.Invoice(from_, invoice_num)
        orm.db.session.add(invoice)
        orm.db.session.commit()
        return invoice
    def getItems(self, store_id):
        results = orm.Item.query.filter_by(store_id=store_id).all()
        return results
    def getItem(self, store_id, name):
        results = orm.Item.query.filter_by(store_id=store_id, name=name).first()
        return results
    def getStorebyPhone(self, phone):
        results = orm.Establishment.query.filter_by(phone=phone).first()
        return results
    def getStorebyEmail(self, email):
        results = orm.Establishment.query.filter_by(email=email).first()
        return results


#dao = Dao()
#print(str(dao.addInvoice("787-391-1464", "testinglala1342")))