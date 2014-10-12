from app import app
from twilio.rest import TwilioRestClient
from dao import Dao
import credentials


dao = Dao()

client = TwilioRestClient(credentials.get_twilio_sid, credentials.get_twilio_token)

@app.route('/venmo', methods=['GET', 'POST'])
def venmo_intercept():
    if request.method == 'POST':
        payment_status = request.json.get('data').get('status')
        if payment_status == 'settled':
            invoice_id = request.json.get('data').get('id')

            invoice = dao.updateInvoice(invoice_id, payment_status)

            phone_number = invoice['from'].strip('-')

            client.messages.create(to=phone_number, from_=credentials.get_twilio_number, body="Pick up yo' coffe brah")
            
    return request.args["venmo_challenge"]