from flask import Flask, render_template, request, send_from_directory, abort
import threading
import time

app = Flask(__name__)

@app.route('/ressources/<path:req>', methods = ['GET'])
def ressource(req):
    return send_from_directory('ressources', req)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

def main():
    pass

if __name__ == "__main__":
    t = threading.Thread(target=main)
    t.start()
    app.run(debug=True, threaded=True)