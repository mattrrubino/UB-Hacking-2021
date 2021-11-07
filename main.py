from flask import Flask, request, abort
from flask_cors import CORS
from twilio.rest import Client
import os
import threading
import socket
import time


app = Flask(__name__)
CORS(app)

# ClearCore private IP and TCP server port
IP = '192.168.1.252'
PORT = 12345
MESSAGE = 'R'.encode()

# Initialize Twilio API
ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
PHONE_NUMBER = '+13375610964'
client = Client(ACCOUNT_SID, AUTH_TOKEN)

COOK_TIME = 300


def ramen_response(from_, to):
    client.messages.create(
        body='Your ramen is being prepared.',
        from_=from_,
        to=to
    )


def ramen_started(from_, to):
    ramen_response(from_, to)

    time.sleep(COOK_TIME)

    client.messages.create(
        body='Your ramen is ready. Enjoy!',
        from_=from_,
        to=to
    )


@app.route('/ramen', methods=['GET', 'POST'])
def ramen():
    body = request.form['Body']
    from_ = request.form['From']
    to = request.form['To']

    if body is None or from_ is None or to is None:
        abort(400)

    if (not 'ramen' in body.lower()):
        return "Message received."

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))
        s.send(MESSAGE)

    thread = threading.Thread(target=ramen_started, args=(to, from_))
    thread.start()

    return "Ramen ordered."
 

app.run(host='192.168.1.179', port=80, debug=False)
