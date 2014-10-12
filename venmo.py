import credentials, requests
from dao import Dao

VENMO_ACCESS_TOKEN = credentials.get_venmo_token()

class Venmo:

  def __init__(self):
    return

  #Once an order is received, create an invoice and charge the customer
  def chargeByPhone(self, user_phone, store_phone, item_order):

    dao = Dao()

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

    store = Dao.getStorebyEmail(store_email)

    item = Dao.getItem(store.id, item_order['name'])

    data = {
      "access_token" : VENMO_ACCESS_TOKEN,
      "email" : user_email,
      "note" : item.description,
      "amount": -1 * item.price
    }

    url = "https://api.venmo.com/v1/payments"
    response = requests.post(url, data)
    if response.status_code == 200:
      invoice_id = response.json.get("payment").get("id")
        #Invoice number
      result = Dao.addInvoice(user_email, invoice_id)
      if result:
        return True
    else:
      return False