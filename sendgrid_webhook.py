from app import app
from dao import Dao
from venmo import Venmo

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
    venmo.chargeByEmail(from_, to, item)
#	for key in result:
#		print('Key: ' + str(key) + ' Result: ' +  result[key])
    print('From: ' + from_ + ' Subject' + subject + ' Message: ' + message)
    return str(request.form)