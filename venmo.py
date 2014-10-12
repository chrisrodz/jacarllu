import credentials, requests
from dao import Dao

VENMO_ACCESS_TOKEN = credentials.get_venmo_token()

class Venmo:

	def __init__(self):
		return

	#Once an order is received, create an invoice and charge the customer
	def charge(self, user_phone, store_phone, item_order):

		store = Dao.getStore(store_phone)

		item = Dao.getItem(store.id, item_order['name'])
	 	
	 	data = {
	 		"access_token" : VENMO_ACCESS_TOKEN,
	 		"phone" : user_phone,
	 		"note" : item.description,
	 		"amount": -1 * item.price
	 	}

	 	url = "https://api.venmo.com/v1/payments"
	 	response = requests.post(url, data)
	 	if response.status_code == 200:
	 		invoice_id = response.json.get("payment").get("id")
	 			#Invoice number
	 		result = Dao.addInvoice(user_phone, invoice_id)
	 		if result:
	 			return True
	 	else:
	 		return False

	def charge(self, user_email, store_email, item_order):

		store = Dao.getStore(store_email)

		item = Dao.getItem(store.id, item_order['name'])

	 	data = {
	 		"access_token" : VENMO_ACCESS_TOKEN,
	 		"phone" : user_email, ################### fix "phone" tag
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