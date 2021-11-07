from flask import Flask, request, abort
from flask_cors import CORS
import socket


app = Flask(__name__)
CORS(app)

# ClearCore private IP and TCP server port
IP = '192.168.1.252'
PORT = 12345
MESSAGE = 'R'.encode()


@app.route('/ramen', methods=['GET', 'POST'])
def ramen():
    body = request.form['Body']

    if body is None:
        abort(400)

    if (not 'ramen' in body.lower()):
        return "Message received."

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))
        s.send(MESSAGE)

    return "Ramen ordered."
 

app.run(host='192.168.1.179', port=80, debug=False)
