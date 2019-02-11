import RPi.GPIO as GPIO

def get_temp(): 
    tfile = open("/sys/bus/w1/devices/10-000802824e58/w1_slave") 
    text = tfile.read() 
    tfile.close() 
    secondline = text.split("\n")[1] 
    temperaturedata = secondline.split(" ")[9] 
    # The first two characters are "t="
    temperature = float(temperaturedata[2:]) 
    temperature = temperature / 1000 
    return temperature

def __main__(): 
    
