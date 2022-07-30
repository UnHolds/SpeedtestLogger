from flask import Flask, render_template, request, send_from_directory, abort
import threading
import speedtest
import datetime
import time
import random

app = Flask(__name__)

@app.route('/ressources/<path:req>', methods = ['GET'])
def ressource(req):
    return send_from_directory('ressources', req)

@app.route('/', methods = ['GET'])
def index():
    timestamps = list(map(lambda x: x[0], measurements[-288:]))
    pingTimes = list(map(lambda x: x[1], measurements[-288:]))
    downloadSpeeds = list(map(lambda x: x[2], measurements[-288:]))
    uploadSpeeds  = list(map(lambda x: x[3], measurements[-288:]))
    return render_template('index.html', timestamps=timestamps, pingTimes=pingTimes, downloadSpeeds=downloadSpeeds, uploadSpeeds=uploadSpeeds)

measurements = []

def main():
    while(True):
        time.sleep(30)
        if(int (datetime.datetime.now().strftime("%M")) % 5 == 0):
            now = datetime.datetime.now().strftime("%Y/%m/%d  %H:%M:%S")
            st = speedtest.Speedtest()
            st.get_best_server()
            
            ping = st.results.ping
            download = round(st.download() / 1000 / 1000, 1)
            upload = round(st.upload() / 1000 / 1000, 1)
            measurements.append((now,ping,download,upload))
            print(measurements)




if __name__ == "__main__":
    t = threading.Thread(target=main)
    t.start()
    app.run(debug=True, threaded=True)

