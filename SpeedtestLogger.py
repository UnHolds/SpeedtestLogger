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
    timestamps = list(map(lambda x: x[0], measurements))
    pingTimes = list(map(lambda x: x[1], measurements))
    downloadSpeeds = list(map(lambda x: x[2], measurements))
    uploadSpeeds  = list(map(lambda x: x[3], measurements))

    avgPingLast24Hour = avg2(pingTimes[-288:])
    avgDownloadLast24Hour = avg2(downloadSpeeds[-288:])
    avgUploadLast24Hour = avg2(uploadSpeeds[-288:])

    avgPing = avg2(pingTimes)
    avgDownload = avg2(downloadSpeeds)
    avgUpload = avg2(uploadSpeeds)
    
    avgPingLastHour = avg2(pingTimes[-12:])
    avgDownloadLastHour = avg2(downloadSpeeds[-12:])
    avgUploadLastHour = avg2(uploadSpeeds[-12:])

    return render_template('index.html', timestamps=timestamps[-288:], pingTimes=pingTimes[-288:], downloadSpeeds=downloadSpeeds[-288:], uploadSpeeds=uploadSpeeds[-288:],
        avgPingLast24Hour=avgPingLast24Hour, avgDownloadLast24Hour=avgDownloadLast24Hour, avgUploadLast24Hour=avgUploadLast24Hour,
        avgPing=avgPing, avgDownload=avgDownload, avgUpload=avgUpload, avgPingLastHour=avgPingLastHour, avgDownloadLastHour=avgDownloadLastHour, avgUploadLastHour=avgUploadLastHour)

measurements = []

def avg2(l):
    if len(l) == 0:
        return -1
    return round(sum(l)/len(l),1)

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

