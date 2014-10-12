from app import app

@app.route('/venmo', methods=['GET', 'POST'])
def venmo_intercept():
    if request.method == 'POST':
        payment_status = request.json.get('data').get('status')
        if payment_status == 'settled':
            print "The payment was completed, send order confirmation"
            return ""
    return request.args["venmo_challenge"]