from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'mailhog'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/send-email')
def send_email():
    sender = 'your-email@example.com'
    recipient = 'recipient-email@example.com'
    subject = 'Hello from Flask!'
    body = 'This is a test email sent from Flask.'

    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = body

    try:
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return 'An error occurred while sending the email: ' + str(e)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)