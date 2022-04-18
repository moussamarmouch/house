import re
import subprocess
import csv
from types import new_class
from flask import Flask, flash,render_template, request


app = Flask(__name__)

# @app.route("/blacklisted")
# def blacklisted():
#     with open('data/blacklist.csv', "w+", newline='') as csvfile3:
#     reader3 = csv.reader(csvfile3, delimiter=';')
#     return "Hello World!"

@app.route("/12")
def titel2():
    mac = []
    host = []
    known = []
    mac_bekend = []
    black = []
    # with open('data/test.csv', "w+", newline='') as csvfile, open('data/known.csv', newline='') as csvfile1, open("data/blacklist.csv", newline = '') as csvfile2:
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
                    if row[5] not in mac_bekend:
                        mac.append(row[5])
                        zin = row[5] + ";" + row[4]
                        host.append(zin)
        csvfile.close

        for know in reader1: 
            if know[0] in mac:
                known.append(know[2])
                mac_bekend.append(know[0])

    csvfile2.close()
    csvfile1.close()

    return render_template('index.html',header='House', mac_list = known, new_mac = host)         

@app.route('/12', methods=['POST'])
def my_form_post():
    text = request.form['name']
    mac = request.form['mac_val']
    processed_text = mac + ";" + text
    with open('data/known.csv', "a") as csvfile1:
        csvfile1.write(processed_text + "\n")
        csvfile1.close()
    return titel2()

@app.route("/blacklist/<mac>", methods = ['POST'])
def blacklist(mac):
    with open("data/blacklist.csv", "a" ) as csvfile2:
        csvfile2.write(mac[:17] + "\n")
        csvfile2.close()
    return titel2()

@app.route("/add_know/<i>", methods = ['POST'])
def add(i):
    with open("data/know.csv", "a" ) as csvfile1:
        csvfile1.write(i + "\n")
        csvfile1.close()
    return True

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
