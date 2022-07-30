from flask import Flask, render_template, request, send_from_directory, abort
import threading
import speedtest
import datetime
import time
import random
from csv import writer
import os

app = Flask(__name__)
started = False

@app.route('/ressources/<path:req>', methods = ['GET'])
def ressource(req):
    return send_from_directory('ressources', req)

@app.route('/', methods = ['GET'])
def index():

    if os.path.exists("thread.lock") == False:
        open("thread.lock", 'a').close()
        t = threading.Thread(target=main)
        t.start()

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

    return render_template('index.html', timestamps=list(map(lambda x: x.split(" - ")[1], timestamps[-288:])), pingTimes=pingTimes[-288:], downloadSpeeds=downloadSpeeds[-288:], uploadSpeeds=uploadSpeeds[-288:],
        avgPingLast24Hour=avgPingLast24Hour, avgDownloadLast24Hour=avgDownloadLast24Hour, avgUploadLast24Hour=avgUploadLast24Hour,
        avgPing=avgPing, avgDownload=avgDownload, avgUpload=avgUpload, avgPingLastHour=avgPingLastHour, avgDownloadLastHour=avgDownloadLastHour, avgUploadLastHour=avgUploadLastHour)

measurements = []

def avg2(l):
    if len(l) == 0:
        return -1
    return round(sum(l)/len(l),1)



def main():

    print("entry")
    lastTest = datetime.datetime.now()
    while(True):
        time.sleep(30)
        if(int (datetime.datetime.now().strftime("%M")) % 5 == 0):
            now = datetime.datetime.now()
            if (now - lastTest > datetime.timedelta(minutes=1)):
                lastTest = now
                try:
                    st = speedtest.Speedtest()
                    st.get_best_server()
                    ping = st.results.ping
                    download = round(st.download() / 1000 / 1000, 1)
                    upload = round(st.upload() / 1000 / 1000, 1)

                    data = (now.strftime("%Y/%m/%d - %H:%M"),ping,download,upload)
                    measurements.append(data)
                
                    with open('data.csv', 'a', newline='') as csv_file:  
                        csv_writer = writer(csv_file)
                        csv_writer.writerow(list(data))  
                        csv_file.close()
                except:
                    print("fail")
                    pass 



if __name__ == "__main__":
    if os.path.exists("thread.lock"):
        os.remove("thread.lock")
    app.run(debug=True, host="0.0.0.0")

