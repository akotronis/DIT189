from flask import Flask, request
from flask_cors import CORS
from flask_mail import Mail, Message
import json

app = Flask(__name__)
# CORS(app)

app.config['MAIL_SERVER'] = 'mailhog'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

CORS(app, support_credentials=True)

sender_email = "consensual.divorce@gmail.com"

states = {
    "INITIALIZED": "Divorce {divorce} was initialized by {role} {name} {surname}.",
    "CONFIRMED": "Divorce {divorce} was confirmed by {role} {name} {surname}.",
    "CANCELLED": "Divorce {divorce} was cancelled by {role} {name} {surname}.",
    "WAITING_PERIOD_STARTED": "10 day waiting period of divorce {divorce} has started.",
    "WAITING_PERIOD_ENDED": "10 day waiting period of divorce {divorce} has ended.",
    "FINALIZED": "Divorce {divorce} is now finalized."
}


@app.route('/send-email', methods=['POST'])
def send_email():
    
    data = request.get_json()

    if "state" in data:
        state = data["state"]
    else:
        return "No state specified!"
    
    if "divorce" in data:
        divorce = data["divorce"]
    else:
        return "No divorce specified!"

    if "user" in data:
        user = data["user"]

        if "name" in user:
            name = user["name"]
        else:
            return "No name of user specified!"
        
        if "surname" in user:
            surname = user["surname"]
        else:
            return "No name of surname specified!"
        
        if "role" in user:
            role = user["role"]
        else:
            return "No role of user specified!"

        if "email" in user:
            email = user["email"]
        else:
            return "No email of user specified!"
    else:
        return "No user specified!"

    if "recipients" in data:
        recipients = data["recipients"]
        if(len(recipients) == 0):
            return "No recipients specified!"
        recipients.insert(0, email)
    else:
        return "No recipients specified!"
    
    msg = Message(state, sender=sender_email, recipients=recipients)
   
    state = state.upper()
    if(state == "INITIALIZED" or state == "CONFIRMED" or state == "CANCELLED"):
        temp = states[state]
        temp = temp.replace("{role}", role)
        temp = temp.replace("{divorce}", divorce)
        temp = temp.replace("{name}", name)
        temp = temp.replace("{surname}", surname)
        msg.body = temp
    elif(state == "WAITING_PERIOD_STARTED" or state == "WAITING_PERIOD_ENDED" or state == "FINALIZED"):
        temp = states[state]
        temp = temp.replace("{divorce}", divorce)
        msg.body = temp
    else:
        return "Unknown state!"

    msg.body = msg.body.replace("{divorce}", divorce)

    try:
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return "An error occurred while sending the email: " + str(e)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5050)