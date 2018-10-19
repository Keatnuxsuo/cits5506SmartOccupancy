from flask import Flask, render_template
import time
import datetime
import RPIO
app = Flask(__name__)

RPIO.setmode(RPIO.BCM)

a_pin = 18
b_pin = 23
buffer = 0
buffer2 = 0

@app.route("/")

def hello():
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        #read sensor status
        sensor = status()
        templateData = {
            'title': 'FRS input Status!',
            'time' : timeString,
            'Sensor' : sensor
            }

        return render_template('index.html', **templateData)

def discharge():
    RPIO.setup(a_pin, RPIO.IN)
    RPIO.setup(b_pin, RPIO.OUT)
    RPIO.output(b_pin, False)
    time.sleep(0.005)

def charge_time():
    RPIO.setup(b_pin, RPIO.IN)
    RPIO.setup(a_pin, RPIO.OUT)
    count = 0
    RPIO.output(a_pin, True)
    while not RPIO.input(b_pin):
        count = count + 1
    return count

def analog_read():
    discharge()
    return charge_time()

def status():
	while True:	
		if analog_read() == 0:
			return("in use")
		else:
			return("free")
	time.sleep(1)
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
