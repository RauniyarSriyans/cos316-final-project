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

def otChange(ogText, newText):
   textTuplesList = tuple(itertools.zip_longest(ogText.splitlines(keepends=True), newText.splitlines(keepends=True), fillvalue = ""))
   #print("Text tupes: ", textTuplesList)
   ogTextList = ogText.splitlines(keepends=True)
   print(ogTextList)
   lineIndex = 0
   transformedText = []
   changefound = False
   changePos = 0

   while not changefound:
      for textStrings in textTuplesList:
        ogTextLine = textStrings[0]
        newTextLine = textStrings[1]

        s = difflib.SequenceMatcher(None, ogTextLine, newTextLine)
        opcodes = s.get_opcodes()

        ogTextLineList = list(ogTextLine)
        # if the op code doesnt == equal then do the if statements?

        tag, i1, i2, j1, j2 = 'string', 0, 0, 0, 0
        for tag, i1, i2, j1, j2 in opcodes:       
          if tag == "delete":
              #print("Delete: {} ".format(ogTextLine[i1:i2]))
              ogTextLineList[i1:i2] = [""] * (i2 - i1)
              changePos+= len(newTextLine)

              ogTextList[lineIndex] = ogTextLineList
              changefound = True
          
          elif tag == "replace":
              #print("Replace: {}  ".format(ogTextLine[i1:i2], newTextLine[j1:j2]))
              ogTextLineList[i1:i2] = newTextLine[j1:j2]
              changePos+= len(newTextLine)

              ogTextList[lineIndex] = ogTextLineList
              changefound = True
          
          elif tag == "insert":
              #print("Insert: {} ".format(newTextLine[j1:j2], i1))
              ogTextLineList.insert(i1, newTextLine[j1:j2])
              changePos+= len(newTextLine)

              ogTextList[lineIndex] = ogTextLineList
              changefound = True
          
          else:
              #changePos+= len(ogTextLine)
              changefound = False
        transformedText.append(''.join(ogTextLineList))
        lineIndex+1

    #basiclaly you want to break once you found the change to keep that position,
      #but now we are not getting the rest of the text post change
        #so we have to figure out a way to get that in :3
   transformedText.append(''.join(ogTextList[lineIndex:]))
   #print("\nTransformed Sequence : ", transformedText)
   return transformedText, changePos


@app.route('/')
def index():
  return render_template('frontend.html')

@socketio.on('new_client')
def handle_connect():
   global document
   print("SOMEONE NEW!")

   if document:
    print("requestoing document")
    emit('receive_document', {'content': document})

@socketio.on('send_change')
def handle_change(data):
    global document
    
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