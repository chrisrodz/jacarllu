import credentials

VENMO_ACCESS_TOKEN = credentials.get_venmo_token()

class Venmo:
	#Once an order is received, create an invoice and charge the customer
	def charge(user_phone, store_phone, item):

		store = Dao.getStore(store_phone)

		item = Dao.getItem(store.id, item['name'])
	 	
	 	data = {
	 		"access_token" : VENMO_ACCESS_TOKEN,
	 		"phone" : user_phone,
	 		"note" : item.description,
	 		"amount": -1 * item.price
	 	}

	 	url = "https://api.venmo.com/v1/payments"
	 	response = requests.post(url, data)
	 	if response.status_code == 200:
	 		return True
	 	else:
	 		return False
