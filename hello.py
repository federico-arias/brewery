from flask import (Flask, Response, render_template)
import json
import threading
import time
import datetime
import random

app = Flask(__name__)

@app.before_first_request
def read_temp_sensor():
    def run_job():
        while True:
            print("Dumping temp data into csv...")
            #with open('/sys/bus/w1/devices/28-011313a1d9aa/w1_slave ', 'r') as t:
            #    temp = float(t.readlines()[-1].split('=')[1]) / 1000
            #with open('temp_data.csv', 'w') as f:
            #    f.write(str(temp) + ', ' + datetime.datetime.now().isoformat() + '\n')
            time.sleep(30)

    thread = threading.Thread(target=run_job)
    thread.start()

@app.route("/")
def index():
    return render_template("index.html")

# this should go directly to the sensor instead of the CSV
@app.route("/api/lasttemp", methods=['GET'])
def temp():
    #with open('/sys/bus/w1/devices/28-011313a1d9aa/w1_slave ', 'r') as t:
    #   temp = float(t.readlines()[-1].split('=')[1]) / 1000
    #js = json.dumps({"datetime": datetime.datetime.now().isoformat(), "temp": temp})
    #return Response(js, status=200, mimetype='application/json')
    return Response(json.dumps([{"datetime":datetime.datetime.now().isoformat(), "temp":4 + random.randint(10,30)}]), status=200, mimetype='application/json')

@app.route("/api/temp", methods=['GET'])
def t():
    ls = []
    with open('temp_data.csv', 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 1800):
            line = lines[i].split(',')
            ls.append({"datetime":line[0], "temp":int(line[1].strip('\n '))})
    return Response(json.dumps(ls), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
