import time
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)

app.debug = True
CORS(app)
socketio = SocketIO(app)

document = [] # global var

@app.route('/')
def index():
  return render_template('frontend.html')

@socketio.on('send_change')
def handle_change(data):
    emit('receive_change', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2000, debug=True)