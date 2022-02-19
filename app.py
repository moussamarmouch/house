import subprocess

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/12")
def titel2():
    subprocess.Popen("fing -r 1 -o log,csv,test.csv", shell=True, stdout=subprocess.PIPE).stdout.read()
    return "test"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
