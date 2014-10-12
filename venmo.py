import credentials, requests
from dao import Dao

VENMO_ACCESS_TOKEN = credentials.get_venmo_token()

dao = Dao()

class Venmo:

  def __init__(self):
    return

  #Once an order is received, create an invoice and charge the customer
  def chargeByPhone(self, user_phone, store_phone, item_order):


    store = dao.getStorebyPhone(store_phone)

    item = dao.getItem(store.id, item_order)

    data = {
      "access_token" : VENMO_ACCESS_TOKEN,
      "phone" : user_phone,
      "note" : item.description,
      "amount": -1 * item.price
    }

    url = "https://api.venmo.com/v1/payments"
    response = requests.post(url, data)

    response_data = response.json()
    if response.status_code == 200:
      invoice_id = response_data["data"]["payment"]["id"]
        #Invoice number
      result = dao.addInvoice(user_phone, invoice_id)
      if result:
        return True
    else:
      return False

  def chargeByEmail(self, user_email, store_email, item_order):

    store = dao.getStorebyEmail("order@estebiflow.bymail.in")
    item = dao.getItem(1, "CL8")

    data = {
      "access_token" : VENMO_ACCESS_TOKEN,
      "email" : user_email,
      "note": item.description,
      "amount": -1 * item.price
    }

    url = "https://api.venmo.com/v1/payments"
    response = requests.post(url, data)
    response_data = response.json()
    if response.status_code == 200:
      print "se cobro por email"
      invoice_id = response_data["data"]["payment"]["id"]
        #Invoice number
      result = dao.addInvoice(user_email, invoice_id)
      if result:
        return True
    else:
      return False
