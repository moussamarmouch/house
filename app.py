import subprocess

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/12")
def titel2():
    result_success = subprocess.check_output(
                ["fling"], shell=True)
    return result_success

if __name__ == "__main__":
    app.run(host='0.0.0.0')
