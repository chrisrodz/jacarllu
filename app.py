from flask import Flask, request
from twilio import twiml

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def hello():
  if request.method == 'POST':
    r = twiml.Response()
    order = request.form['Body']
    if menu.has_key(order):
      r.message('Ordered %s' % menu[order]['name'])
    elif order == 'MENU':
      m = ''
      for key,value in menu.iteritems():
        m += 'Name: ' + value['name'] + ' Price: $' + str(value['price']) + ' Code: ' + key + '\n\n'
      r.message(m)
    else:
      r.message('No item for that key.\n\n Send MENU for list of items.')
    return str(r)

  return 'Hola'

if __name__ == '__main__':
  app.run(debug=True)