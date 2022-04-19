import re
import subprocess
import csv
from flask import Flask, flash,render_template, request


app = Flask(__name__)

@app.route("/12")
def titel2():
    bekend = []
    bek = []
    scan = []
    known = []
    online= []
    black = []
    offline= []
    mac = []
    new = []
    with open('data/scan.csv', "w+", newline='') as scanfile, open('data/known.csv', newline='') as knownfile, open("data/blacklist.csv", newline = '') as blackfile:
    # with open('data/scan.csv', newline='') as scanfile, open('data/known.csv', newline='') as knownfile, open("data/blacklist.csv", newline = '') as blackfile:
        subprocess.Popen("fing -r 1 -o log,csv,data/scan.csv", shell=True, stdout=subprocess.PIPE).stdout.read() 
        scan_file = csv.reader(scanfile, delimiter=';')
        known_file = csv.reader(knownfile, delimiter=';')
        black_file = csv.reader(blackfile, delimiter=";")
        
        # add mac to blaclist
        for i in black_file:
            black.append(i[0])


        #add macs from scan
        for i in scan_file:
            zin = i[5] + ";" + i[4] + ";" + i[6]
            scan.append(zin)
            bekend.append(i[5])
            #naam+mac

        
       #add macs to known 
        for i in known_file:
            zin = i[0] + ";" + i[3]
            bek.append(i[0])
            known.append(zin)
    

        #online list
        for mac in known:
            if mac[:17] not in black:
                if mac[:17] in bekend:
                    online.append(mac)
        

        #offline list
        for mac_add in known:
            if mac_add[:17] not in black:
                if mac_add[:17] not in bekend:
                    offline.append(mac_add)


        #new mac list
        for macc in scan:
            if macc[:17] not in black:
                if macc[:17] not in bek:
                    new.append(macc)


# cursor parking
# 

#             
    scanfile.close()
    knownfile.close()
    blackfile.close()

    
    return render_template('index.html',header='House', mac_list = online, offline=offline, new_mac =  new)

@app.route("/blacklist")
def blacklisted():
    macs = []
    with open('data/blacklist.csv', "r", newline='') as csvfile3:
        reader3 = csv.reader(csvfile3, delimiter=';')
        #blacklisted mac addressen
        for mac_black in reader3:
            macs.append(mac_black)
        
    csvfile3.close()
        

    return render_template('blacklist.html',header='Blacklist', blacklist_mac = macs)
         

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
    return titel2()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
