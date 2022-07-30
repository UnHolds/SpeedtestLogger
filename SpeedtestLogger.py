from flask import Flask, render_template, request, send_from_directory, abort
import speedtest
import datetime
import time

app = Flask(__name__)

@app.route('/ressources/<path:req>', methods = ['GET'])
def ressource(req):
    return send_from_directory('ressources', req)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

measurements = []

def main():
    while(True):
        print("Test")
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
    #app.run(debug=True)
    main()

