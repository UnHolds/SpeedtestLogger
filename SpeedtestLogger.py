from flask import Flask, render_template, request, send_from_directory, abort

app = Flask(__name__)

@app.route('/ressources/<path:req>', methods = ['GET'])
def ressource(req):
    return send_from_directory('ressources', req)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)