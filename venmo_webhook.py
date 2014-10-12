from app import app
from twilio.rest import TwilioRestClient
from dao import Dao
import credentials
import re
from emails import Emails


dao = Dao()

client = TwilioRestClient(credentials.get_twilio_sid, credentials.get_twilio_token)

email = Emails()

@app.route('/venmo', methods=['GET', 'POST'])
def venmo_intercept():
    if request.method == 'POST':
        payment_status = request.json.get('data').get('status')
        if payment_status == 'settled':
            invoice_id = request.json.get('data').get('id')

            invoice = dao.updateInvoice(invoice_id, payment_status)

            #Check to see if email or phone number
            has_email = re.search('@', invoice['from'])

            if has_email:
                message = "Pick up your coffee brah"
                email.send_email(invoice['from'], message)
            else:
                phone_number = invoice['from'].strip('-')
                client.messages.create(to=phone_number, from_=credentials.get_twilio_number, body="Pick up yo' coffe brah")
            
    return request.args["venmo_challenge"]