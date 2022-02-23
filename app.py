import subprocess
import csv
from types import new_class
from flask import Flask, flash,render_template


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/12")
def titel2():
    mac = []
    known = []
    black = []
    with open('data/test.csv', newline='') as csvfile, open('data/known.csv', newline='') as csvfile1, open("data/blacklist.csv", newline = '') as csvfile2:
        # subprocess.Popen("fing -r 1 -o log,csv,data/test.csv", shell=True, stdout=subprocess.PIPE).stdout.read() 
        reader = csv.reader(csvfile, delimiter=';')
        reader1 = csv.reader(csvfile1, delimiter=';')
        reader2 = csv.reader(csvfile2, delimiter=";")

        for i in reader2:
            black.append(i[0])
        for row in reader:
            if row[5] not in mac:
                if row[5] not in black:
                    mac.append(row[5])
        csvfile.close

        for know in reader1: 
            if know[0] in mac:
                known.append(know[1])

    csvfile2.close()
    csvfile1.close()

    return render_template('index.html',header='House', mac_list = known, new_mac = mac)         

@app.route("/blacklist/<x>", methods = ['POST'])
def blacklist(x):
    with open("data/blacklist.csv", "a" ) as csvfile2:
        csvfile2.write(x + "\n")
        csvfile2.close()
    return True

@app.route("/add_know/<i>", methods = ['POST'])
def add(i):
    with open("data/know.csv", "a" ) as csvfile1:
        csvfile1.write(i + "\n")
        csvfile1.close()
    return True

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
