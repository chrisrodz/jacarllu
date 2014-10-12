from flask import Flask, request, json
import Dao, Venmo

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/webhook', methods=['POST'])
def handle_order():
    result = request.form
    jsons = json.loads(result['envelope'])
    from_ = jsons['from']
    to = jsons['to']
    message = result['text']
    subject = result['subject']
    dao = Dao()
    store = dao.getStore(to)
    #check if store exists
    item = dao.getItem(subject.trim(), store.email)
    #send venmo payment
    venmo = Venmo();
    venmo.charge(from_, to, item)
#	for key in result:
#		print('Key: ' + str(key) + ' Result: ' +  result[key])
    print('From: ' + from_ + ' Subject' + subject + ' Message: ' + message)
    return str(request.form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')