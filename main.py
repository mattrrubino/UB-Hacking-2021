from flask import Flask
from flask_cors import CORS
import socket

app = Flask(__name__)
CORS(app)

# TCP host name
IP = ''
PORT = 12345
MESSAGE = 'RAMEN'

@app.route('/')
def main():
    return "Hello"

@app.route('/ramen', methods=['GET', 'POST'])
def ramen():
    # Intercept message contents

    print("Ramen time!")

    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #    s.connect((IP, PORT))
    #    s.send(MESSAGE)

    return "Success"
 
app.run(host='192.168.1.179', port=80, debug=False)
