import credentials

VENMO_ACCESS_TOKEN = credentials.get_venmo_token()

class Venmo:
	#Once an order is received, create an invoice and charge the customer
	def charge(phone, item):

	  data = {
	  "access_token" : VENMO_ACCESS_TOKEN,
	  "phone" : phone,
	  "note" : item['name'],
	  "amount": -1 * item['price']
	  }

	  url = "https://api.venmo.com/v1/payments"

	  response = requests.post(url, data)
	  if response.status_code == 200:
	    #Charge was successfully made
	    return True
	  else:
	    #There was an error
	    return False
