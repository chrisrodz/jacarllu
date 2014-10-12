from flask import Flask, request
from twilio import twiml
import requests
import json
from venmo import Venmo
import credentials
from dao import Dao
from twilio.rest import TwilioRestClient
from emails import Emails

app = Flask(__name__)

# import venmo_webhook

dao = Dao()

client = TwilioRestClient(credentials.get_twilio_sid(), credentials.get_twilio_token())

email = Emails()

@app.route('/venmo', methods=['GET', 'POST'])
def venmo_intercept():
    if request.method == 'POST':
        payment_status = request.json.get('data').get('status')
        if payment_status == 'settled':
            invoice_id = request.json.get('data').get('id')

            invoice = dao.updateInvoice(invoice_id, payment_status)

            #Check to see if email or phone number
            has_email = '@' in invoice.from_

            if has_email:
                message = "Pick up your coffee brah"
                email.send_email(invoice.from_, message)
            else:
                phone_number = str(invoice.from_)
                client.messages.create(to=phone_number, from_=credentials.get_twilio_number(), body='Pick up yo coffee brah')
                client.messages.create(to="7874526702", from_=credentials.get_twilio_number(), body='Order up! Time to brew!')
    return request.args["venmo_challenge"]

# import sendgrid_webhook

@app.route('/webhook', methods=['POST'])
def handle_order():
    result = request.form
    jsons = json.loads(result['envelope'])
    from_ = jsons['from']
    to = jsons['to']
    message = result['text']
    subject = result['subject']
    dao = Dao()
    store = dao.getStorebyEmail(to)
    #check if store exists
    item = dao.getItem(subject.strip(), "order@estebiflow.bymail.in")
    #send venmo payment
    venmo = Venmo();
    venmo.chargeByEmail(from_, to, message)
# for key in result:
#   print('Key: ' + str(key) + ' Result: ' +  result[key])
    print('From: ' + from_ + ' Subject' + subject + ' Message: ' + message)
    return str(request.form)

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
  'FOR12': {
    'price': 1.25,
    'name': 'Oreo Frappe 12oz.'
  }
}

# Method to handle text messages with orders
def handle_order(order):
  r = twiml.Response()
  if order["body"] == 'MENU':
    m = ''
    for key,value in menu.iteritems():
      m += 'Name: ' + value['name'] + ' Price: $' + str(value['price']) + ' Code: ' + key + '\n\n'
    r.message(m)
  elif venmo.chargeByPhone(order['phone_number'], credentials.get_twilio_number(), order['body']):
    # TODO: Send paypal invoice for item here
    r.message('Ordered %s' % order['body']) # This should be the invoice info
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
  app.run(debug=True, host="0.0.0.0", port=80)
