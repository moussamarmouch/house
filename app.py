import subprocess

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/12")
def titel2():
    return subprocess.Popen("fing", shell=True, stdout=subprocess.PIPE).stdout.read()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
