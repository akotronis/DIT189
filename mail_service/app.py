from flask import Flask, request
from flask_mail import Mail, Message
import json

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'mailhog'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

body = 'This is a test email sent from Flask.'

@app.route('/send-email', methods=['POST'])
def send_email():
    
    # Load the JSON data from the request
    data = request.get_json()

    # Update the email data if provided in the JSON
    if 'sender' in data:
        sender = data['sender']
    else:
        return 'No sender specified!'
    
    if 'recipients' in data:
        recipients = data['recipients']
    else:
        return 'No recipients specified!'
    
    if 'subject' in data:
        subject = data['subject']
    else:
        return 'No subject specified!'

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body

    try:
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return 'An error occurred while sending the email: ' + str(e)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)