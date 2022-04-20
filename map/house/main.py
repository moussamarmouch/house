import subprocess
import re
import csv
from flask_login import login_required, current_user
from flask import Flask, Blueprint, flash, render_template, request

from house.auth import login


main = Blueprint('main', __name__)

# @main.route('/')
# @login_required
# def index():
#     return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route("/")
@login_required
def index():
    bekend = []
    bek = []
    scan = []
    known = []
    online= []
    black = []
    offline= []
    mac = []
    new = []
    with open('house/data/scan.csv', "w+", newline='') as scanfile, open('house/data/known.csv', newline='') as knownfile, open("house/data/blacklist.csv", newline = '') as blackfile:
    # with open('house/data/scan.csv', newline='') as scanfile, open('house/data/known.csv', newline='') as knownfile, open("house/data/blacklist.csv", newline = '') as blackfile:
        subprocess.Popen("fing -r 1 -o log,csv,house/data/scan.csv", shell=True, stdout=subprocess.PIPE).stdout.read() 
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

@main.route("/known")
@login_required
def known():
    macs = []
    with open('house/data/known.csv', "r", newline='') as csvfile3:
        known = csv.reader(csvfile3, delimiter=';')
        #blacklisted mac addressen
        for mac_known in known:
            macs.append(mac_known)
        
    csvfile3.close()
    return render_template('known.html',header='Known Macs', known_mac = macs)



@main.route("/blacklist")
@login_required
def blacklisted():
    macs = []
    with open('house/data/blacklist.csv', "r", newline='') as csvfile3:
        reader3 = csv.reader(csvfile3, delimiter=';')
        #blacklisted mac addressen
        for mac_black in reader3:
            l = str(mac_black).strip("[").strip("]").strip("'")
            macs.append(l)
        
    csvfile3.close()
    return render_template('blacklist.html',header='Blacklist', blacklist_mac = macs)
         

@main.route('/', methods=['POST'])
@login_required
def my_form_post():
    text = request.form['name']
    mac = request.form['mac_val']
    processed_text = mac + ";" + text
    with open('house/data/known.csv', "a") as csvfile1:
        csvfile1.write(processed_text + "\n")
        csvfile1.close()
    return index()

@main.route("/blacklist/<mac>", methods = ['POST'])
@login_required
def blacklist(mac):
    with open("house/data/blacklist.csv", "a" ) as csvfile2:
        csvfile2.write(mac[:17] + "\n")
        csvfile2.close()
    return index()

@main.route("/remblack/<mac>", methods = ['POST'])
@login_required
def remove(mac):
    with open("house/data/blacklist.csv", "r") as csvfile5:
        z = csvfile5.readlines()
        z.remove(mac)
        # reader6 = csv.reader(csvfile5, delimiter=';')
        # for i in reader6:
            
        csvfile5.close()
    return index()

@main.route("/add_know/<i>", methods = ['POST'])
@login_required
def add(i):
    with open("house/data/know.csv", "a" ) as csvfile1:
        csvfile1.write(i + "\n")
        csvfile1.close()
    return index()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', debug=True)
