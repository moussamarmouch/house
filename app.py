import subprocess
import csv
from flask import Flask,render_template
from flask_debugtoolbar import DebugToolbarExtension
import logging
from mac_vendor_lookup import MacLookup

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/12")
def titel2():
    mac = []
    known = []
    subprocess.Popen("fing -r 1 -o log,csv,data/test.csv", shell=True, stdout=subprocess.PIPE).stdout.read()
    with open('data/test.csv', newline='') as csvfile, open('data/known.csv', newline='') as csvfile1:
        reader = csv.reader(csvfile, delimiter=';')
        reader1 = csv.reader(csvfile1, delimiter=';')
        for row in reader:
            mac.append(row[5])
        csvfile.close
        for know in reader1: 
            if know[0] in mac:
                known.append(know[1])
    csvfile1.close
    return render_template('index.html',header='House', mac_list = known)               

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
