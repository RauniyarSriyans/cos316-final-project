import time
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import difflib
from pprint import pprint
import itertools
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

app.debug = True
CORS(app)
socketio = SocketIO(app)

document = ""
#clients = set() # set of clients

def checkChange(ogText, newText):
   textTuplesList = tuple(itertools.zip_longest(ogText.splitlines(keepends=True), newText.splitlines(keepends=True), fillvalue = ""))
   print("Text tupes: ", textTuplesList)

   transformedText = []

   for textStrings in textTuplesList:
      ogTextLine = textStrings[0]
      newTextLine = textStrings[1]

      s = difflib.SequenceMatcher(None, ogTextLine, newTextLine)
      opcodes = s.get_opcodes()

      ogTextLineList = list(ogTextLine)

      #print("OG LINE", ogTextLineList)
      for tag, i1,i2,j1,j2 in opcodes:
        if tag == "delete":
            print("Delete: {} ".format(ogTextLine[i1:i2]))
            ogTextLineList[i1:i2] = [""] * (i2 - i1)
        elif tag == "replace":
            print("Replace: {}  ".format(ogTextLine[i1:i2], newTextLine[j1:j2]))
            ogTextLineList[i1:i2] = newTextLine[j1:j2]
        elif tag == "insert":
            print("Insert: {} ".format(newTextLine[j1:j2], i1))
            ogTextLineList.insert(i1, newTextLine[j1:j2])
        elif tag == "equal":
            print("Equal : {} ".format(ogTextLine[i1:i2]))
      transformedText.append(''.join(ogTextLineList))
    
   print("\nTransformed Sequence : ", transformedText)
   return transformedText


@app.route('/')
def index():
  return render_template('frontend.html')

@socketio.on('new_client')
def handle_connect():
   global document
   print("SOMEONE NEW!")
   #clients.add(request.sid)
   if document:
    print("requestoing document")
    emit('receive_document', {'content': document})

@socketio.on('send_change')
def handle_change(data):
    global document
    
    #print("data changed: ", data['content'])
    #print("document: ", document)
    transformedDoc = checkChange(document, data["content"])

    #convert it back into a single string
    combinedText = ''.join(transformedDoc)
    document =  data["content"]
    #print("THIS IS THE FORMATING", (data['content']))
    #print("COMBEIND TEXT", combinedText)

    #ot_document = ot_changes(data['content'], document)
    emit('receive_document', {'content': combinedText}, broadcast=True, include_self=True)

@socketio.on('disconnect')
def handle_disconnect():
  print('disconnected ):')
  #print(clients)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=2000, debug=True)