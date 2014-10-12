from flask import Flask, request
from twilio import twiml
import requests
from venmo import Venmo
import credentials

app = Flask(__name__)

import venmo_webhook

import sendgrid_webhook

venmo = Venmo()


menu = {
  'CL8': {
    'price': 2,
    'name': 'Latte Coffee 8oz.'
  },
  'CL12': {
    'price': 3.5,
    'name': 'Latte Coffee 12oz.'
  },
  'WATER': {
    'price': 1.25,
    'name': 'Bottle of Water 16oz.'
  }
}

# Method to handle text messages with orders
def handle_order(order):
  r = twiml.Response()
  print order['phone_number']
  print "Something?"
  if venmo.chargeByPhone(order['phone_number'], credentials.get_twilio_number(), order['body']):
    # TODO: Send paypal invoice for item here
    r.message('Ordered %s' % order['body']) # This should be the invoice info
  elif order == 'MENU':
    m = ''
    for key,value in menu.iteritems():
      m += 'Name: ' + value['name'] + ' Price: $' + str(value['price']) + ' Code: ' + key + '\n\n'
    r.message(m)
  else:
    r.message('No item for that key.\n\n Send MENU for list of items.')
  return str(r)

@app.route('/', methods=['POST'])
def hello():
  order = {
  "body" : request.form['Body'],
  "phone_number" : request.form['From']
  }

  return handle_order(order)

if __name__ == '__main__':
  app.run(debug=True)