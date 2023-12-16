import time
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import difflib
from pprint import pprint
import itertools
import logging
import datetime


log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)

app.debug = True
CORS(app)
socketio = SocketIO(app)

document = ""

def otChange(ogText, newText):

  s = difflib.SequenceMatcher(None, ogText, newText)
  opcodes = s.get_opcodes()
  changePos = 0

  transformedText = list(ogText)

  for tag, i1, i2, j1, j2 in opcodes:       
    if tag == "delete":
        transformedText[i1:i2] = [""] * (i2 - i1)
        changePos = i1
    
    elif tag == "replace":
        transformedText[i1:i2] = newText[j1:j2]
        changePos = i2

    elif tag == "insert":
        transformedText.insert(i1, newText[j1:j2])
        changePos = i2

  return transformedText, changePos


@app.route('/')
def index():
  return render_template('frontend.html')

@socketio.on('new_client')
def handle_connect():
  global document
  print("SOMEONE NEW!")

  if document:
    print("requesting document")
    emit('receive_document', {'content': document})

@socketio.on('send_change')
def handle_change(data):
    global document
    frontend_timestamp = data['time']
    # Get the server-side timestamp
    server_timestamp = time.time() * 1000  # Convert to millisecond
    print(server_timestamp)
    # Calculate the time delay
    time_delay = server_timestamp - frontend_timestamp
    print("Delay (in ms): ", time_delay)
    transformedDoc, changePos = otChange(document, data["content"])
    print("change position: ", changePos)
    #convert it back into a single string
    combinedText = ''.join(transformedDoc)
    document = data["content"]

    emit('receive_document_change', {'content': combinedText, 'pos': changePos}, broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
  print('disconnected ):')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2000, debug=True)
