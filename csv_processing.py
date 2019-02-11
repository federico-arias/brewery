import threading
from datetime import datetime as dt
from datetime import timedelta as delta
import random 
import json

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def append_time():
    iso = dt.now().isoformat()
    with open('temp_data.csv', 'a') as f:
        f.write(iso, + ', ' + str(random.randint(20, 50)) + '\n')

def read_time():
    with open('temp_data.csv', 'r') as f:
        last_line = f.readlines()[-1].split(',')
    timedate = last_line[0]
    temp = last_line[1].strip('\n ') 
    return json.dumps({"datetime": timedate, "temp": temp})

def populate_csv():
    now = dt.now()
    with open('temp_data.csv', 'a') as f:
        for i in reversed(range(350000)):
            t = now - delta(seconds=i)
            f.write(t.isoformat() + ', ' + str(random.randint(0, 50)) + '\n')


#if __name__ == '__main__':
    #print(read_time())
populate_csv()

#app = set_interval(1, append_time)

