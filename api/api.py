import time
from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)

app.debug = True
CORS(app)

document = [] # global var

@app.route('/')
def index():
    return {'data': json.dumps(document)}

@app.route('/data', methods=['POST'])
def data():
  data = json.loads(request.data)
  document.append(data["keycode"])
  print(data, type(data))
  return {'data': "Ello Guvnor"}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}