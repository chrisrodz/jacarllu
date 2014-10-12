import sendgrid

class Emails:
    def __init__(self):
        self.sg = sendgrid.SendGridClient('Zaiber', 'Be7yuseK')
        self.message_subject = 'Our App Subject'
        self.message_from = 'someone@somewhere.com'

    def send_email(self, address, text):
        message = sendgrid.Mail()
        message.add_to(address)
        message.set_subject(self.message_subject)
        message.set_text(text)
        message.set_from(self.message_from)
        status, msg = self.sg.send(message)

#emails = Emails()
#emails.send_email('***REMOVED***','Aloha')