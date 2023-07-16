from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import json

app = Flask(__name__)
cors = CORS(app)
mail = Mail(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAIL_SERVER'] = 'mailhog'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False

sender_email = "consensual.divorce@gmail.com"

states = {
    "INITIALIZED": "Divorce {divorce} was initialized by {role} {name} {surname}.",
    "CONFIRMED": "Divorce {divorce} was confirmed by {role} {name} {surname}.",
    "CANCELLED": "Divorce {divorce} was cancelled by {role} {name} {surname}.",
    "WAITING_PERIOD_STARTED": "10 day waiting period of divorce {divorce} has started.",
    "WAITING_PERIOD_ENDED": "10 day waiting period of divorce {divorce} has ended.",
    "FINALIZED": "Divorce {divorce} is now finalized."
}

@app.route('/send-email', methods=['POST', 'OPTIONS'])
@cross_origin()
def send_email():
    
    data = request.get_json()

    if "state" in data:
        state = data["state"]
    else:
        response = {"error": "No state specified!"}
        return jsonify(response), 400
    
    if "divorce" in data:
        divorce = data["divorce"]
    else:
        response = {"error": "No divorce specified!"}
        return jsonify(response), 400

    if "user" in data:
        user = data["user"]

        if "name" in user:
            name = user["name"]
        else:
            response = {"error": "No name of user specified!"}
            return jsonify(response), 400
        
        if "surname" in user:
            surname = user["surname"]
        else:
            response = {"error": "No name of surname specified!"}
            return jsonify(response), 400
        
        if "role" in user:
            role = user["role"]
        else:
            response = {"error": "No role of user specified!"}
            return jsonify(response), 400

        if "email" in user:
            email = user["email"]
        else:
            response = {"error": "No email of user specified!"}
            return jsonify(response), 400
    else:
        response = {"error": "No user specified!"}
        return jsonify(response), 400

    if "recipients" in data:
        recipients = data["recipients"]
        if(len(recipients) == 0):
            response = {"error": "No recipients specified!"}
            return jsonify(response), 400
        recipients.insert(0, email)
    else:
        response = {"error": "No recipients specified!"}
        return jsonify(response), 400
    
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
        response = {"error": "Unknown state!"}
        return jsonify(response), 400

    msg.body = msg.body.replace("{divorce}", divorce)

    try:
        mail.send(msg)
        response = {"message": "Email sent successfully!"}
        return jsonify(response), 200
    except Exception as e:
        response = {"error": "An error occurred while sending the email: " + str(e)}
        return jsonify(response), 400
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5050)