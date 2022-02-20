import subprocess
import csv
from flask import Flask,render_template
from mac_vendor_lookup import MacLookup
app = Flask(__name__)

MacLookup().update_vendors()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/12")
def titel2():
    mac = []
    subprocess.Popen("fing -r 1 -o log,csv,data/test.csv", shell=True, stdout=subprocess.PIPE).stdout.read()
    with open('data/test.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            try:
                vendor = MacLookup().lookup(row[5])
            except KeyError:
                vendor = " "
            yes = (row[5], vendor)
            mac.append(yes)
        csvfile.close
    return render_template('index.html',header='House', mac_list = mac)               

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
