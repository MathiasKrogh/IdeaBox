from http import server
from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template
from gevent.pywsgi import WSGIServer
import pyrebase
from gpiozero.pins.pigpio import PiGPIOFactory
import random
import gpiozero
# from gpiozero import Servo
from time import sleep

app = Flask(__name__, template_folder='templates')
app.secret_key = "goodkey"

# Firebase configuration
firebaseConfig={"apiKey": "AIzaSyC35JQhDJu6JpPUh5UelWToZPa-g3dnlJ4",
  "authDomain": "idea-box-ef8e8.firebaseapp.com",
  "databaseURL": "https://idea-box-ef8e8-default-rtdb.europe-west1.firebasedatabase.app/",
  "projectId": "idea-box-ef8e8",
  "storageBucket": "idea-box-ef8e8.appspot.com",
  "messagingSenderId": "186666334977",
  "appId": "1:186666334977:web:5734a65add2707495d3900",
  "measurementId": "G-Y4SE07Y0TJ"}

# Use the application default credentials
firebase=pyrebase.initialize_app(firebaseConfig)

firedb=firebase.database()

# GPIO setup
factory = PiGPIOFactory(host='192.168.8.87')
# myCorrection=0.45
# maxPW=(2.0+myCorrection)/1000
# minPW=(1.0-myCorrection)/1000

rightSwitch = gpiozero.DigitalInputDevice("GPIO17",pin_factory=factory)
leftSwitch = gpiozero.DigitalInputDevice("GPIO27",pin_factory=factory)
phoneSwitch = gpiozero.DigitalInputDevice("GPIO22",pin_factory=factory)
lengthSwitch = gpiozero.DigitalInputDevice("GPIO23",pin_factory=factory)
runSwitch = gpiozero.DigitalInputDevice("GPIO24",pin_factory=factory)
# leftServo = Servo("GPIO5",min_pulse_width=minPW,max_pulse_width=maxPW,pin_factory=factory)
# rightServo = Servo("GPIO12",min_pulse_width=minPW,max_pulse_width=maxPW,pin_factory=factory)
GreenLED1 = gpiozero.LED("GPIO21",pin_factory=factory)
GreenLED2 = gpiozero.LED("GPIO20",pin_factory=factory)
GreenLED3 = gpiozero.LED("GPIO16",pin_factory=factory)
GreenLED4 = gpiozero.LED("GPIO26",pin_factory=factory)
GreenLED5 = gpiozero.LED("GPIO19",pin_factory=factory)
GreenLED6 = gpiozero.LED("GPIO13",pin_factory=factory)
GreenLED7 = gpiozero.LED("GPIO6",pin_factory=factory)
LEDList = [
    GreenLED1,
    GreenLED2,
    GreenLED3,
    GreenLED4,
    GreenLED5,
    GreenLED6,
    GreenLED7
]

activityList = [
    "Language",
    "Relations",
    "Food",
    "Other",
    "Music",
    "Games",
    "Sports"
]

activityLED = 3

##############################
# all different urls

@app.route("/putdownphone")
def render_putdownphone():
    return render_template("PutDownPhone.html")

@app.route("/readyforactivity")
def render_readyforactivity():
    return render_template("ReadyForActivity.html")

@app.route("/notready")
def render_notready():
    return render_template("NotReady.html")

@app.route("/pullthelever")
def render_pullthelever():
    return render_template("PullTheLever.html")

@app.route("/pullanimation")
def render_pullanimation():
    activity = activityString
    return render_template("PullAnimation.html", activity = activity)

@app.route("/activitycountdown")
def render_activitycountdown():
    activity = activityString
    return render_template("ActivityCountdown.html", activity = activity)

@app.route("/activitycomplete")
def render_activitycomplete():
    return render_template("ActivityComplete.html")

##############################
# Background activity on some pages

@app.route("/listenactivity")
def listenactivity():
    def respond_to_client1():
        rightSwitchStatus = rightSwitch.value
        leftSwitchStatus = leftSwitch.value
        if leftSwitchStatus == 1:
            if activityLED == 6:
                activityLED = 0
            else:
                activityLED = activityLED + 1
        if rightSwitchStatus == 1:
            if activityLED == 0:
                activityLED = 6
            else:
                activityLED = activityLED - 1
        LEDList[activityLED].on()
        if activityLED != 0:
            LEDList[activityLED-1].off()
        else:
            LEDList[6].off()
        if activityLED != 6:
            LEDList[activityLED+1].off()
        else:
            LEDList[0].off()
        activityType = activityList[activityLED]
        lengthSwitchStatus = lengthSwitch.value
        if runSwitch.value == 1:
            activitiesDatabase = firedb.child("activities").get()
            newlist = []
            for activity in activitiesDatabase.each():
                if activityType != "Random":
                    if activity.val()["type"] == activityType and activity.val()["long"] == lengthSwitchStatus:
                        newlist.append(activity.val())
                else:
                    if activity.val()["long"] == lengthSwitchStatus:
                        newlist.append(activity.val())
            randActivity = random.choice(newlist)
            global activityString
            activityString = randActivity["type"] + ": " + randActivity["desc"]   
            activityLED = 3
            yield f"id: 1\ndata: {activityString}\nevent: newactivity\n\n"
            sleep(5)
        sleep(0.075)
    return Response(respond_to_client1(), mimetype='text/event-stream')
  
@app.route("/listenphonedown")
def render_listenphonedown():
    def respond_to_client2():
        while True:
            phoneSwitchStatus = phoneSwitch.value
            if phoneSwitchStatus == 1:
                _data = "Phone is on the weight!"
                yield f"id: 2\ndata: {_data}\nevent: phoneon\n\n"
    return Response(respond_to_client2(), mimetype='text/event-stream')

@app.route("/listenphoneup")
def render_listenphoneup():
    def respond_to_client3():
        while True:
            phoneSwitchStatus = phoneSwitch.value
            if phoneSwitchStatus == 0:
                _data = "Phone is off the weight!"
                yield f"id: 3\ndata: {_data}\nevent: phoneoff\n\n"
    return Response(respond_to_client3(), mimetype='text/event-stream')

# @app.route("/servoclose")
# def render_servoclose():
#     leftServo.mid()
#     rightServo.mid()
#     return render_template('ReadyForActivity.html')
                

# @app.route("/servoopen")
# def render_servoopen():
#     leftServo.max()
#     rightServo.min()
#     return render_template("ActivityCountdown.html")

##############################
if __name__ == "__main__":
    http_server = WSGIServer(("localhost", 5001), app)
    http_server.serve_forever()