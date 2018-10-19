from flask import Flask, render_template
import time
import datetime
import RPi.GPIO as GPIO
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

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
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.005)

def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    count = 0
    GPIO.output(a_pin, True)
    while not GPIO.input(b_pin):
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
