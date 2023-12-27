# from gevent import monkey; monkey.patch_all()
# from gpiozero.pins.pigpio import PiGPIOFactory
# import random
# import gpiozero
# from time import sleep

# factory = PiGPIOFactory(host='192.168.8.87')
# myCorrection=0.45
# maxPW=(2.0+myCorrection)/1000
# minPW=(1.0-myCorrection)/1000

# rightSwitch = gpiozero.DigitalInputDevice("GPIO17",pin_factory=factory)
# leftSwitch = gpiozero.DigitalInputDevice("GPIO27",pin_factory=factory)
# phoneSwitch = gpiozero.DigitalInputDevice("GPIO22",pin_factory=factory)
# lengthSwitch = gpiozero.DigitalInputDevice("GPIO23",pin_factory=factory)
# runSwitch = gpiozero.DigitalInputDevice("GPIO24",pin_factory=factory)
# leftServo = gpiozero.Servo("GPIO5",min_pulse_width=minPW,max_pulse_width=maxPW,pin_factory=factory)
# rightServo = gpiozero.Servo("GPIO12",min_pulse_width=minPW,max_pulse_width=maxPW,pin_factory=factory)
# GreenLED1 = gpiozero.LED("GPIO21",pin_factory=factory)
# GreenLED2 = gpiozero.LED("GPIO20",pin_factory=factory)
# GreenLED3 = gpiozero.LED("GPIO16",pin_factory=factory)
# GreenLED4 = gpiozero.LED("GPIO26",pin_factory=factory)
# GreenLED5 = gpiozero.LED("GPIO19",pin_factory=factory)
# GreenLED6 = gpiozero.LED("GPIO13",pin_factory=factory)
# GreenLED7 = gpiozero.LED("GPIO6",pin_factory=factory)
# LEDList = [
#     GreenLED1,
#     GreenLED2,
#     GreenLED3,
#     GreenLED4,
#     GreenLED5,
#     GreenLED6,
#     GreenLED7
# ]

# activityList = [
#     "Language",
#     "Relations",
#     "Food",
#     "Random",
#     "Music",
#     "Games",
#     "Sport"
# ]

# activityLED = 3

# rightSwitchStatus = rightSwitch.value
# leftSwitchStatus = leftSwitch.value
# if leftSwitchStatus == 1:
#     if activityLED == 6:
#         activityLED = 0
#     else:
#         activityLED = activityLED + 1
# if rightSwitchStatus == 1:
#     if activityLED == 0:
#         activityLED = 6
#     else:
#         activityLED = activityLED - 1
# LEDList[activityLED].on()
# if activityLED != 0:
#     LEDList[activityLED-1].off()
# else:
#     LEDList[6].off()
# if activityLED != 6:
#     LEDList[activityLED+1].off()
# else:
#     LEDList[0].off()
# activityType = activityList[activityLED]
# lengthSwitchStatus = lengthSwitch.value
# if runSwitch.value == 1:
#     activitiesDatabase = firedb.child("activities").get()
#     newlist = []
#     for activity in activitiesDatabase.each():
#         if activityType != "Random":
#             if activity.val()["type"] == activityType and activity.val()["long"] == lengthSwitchStatus:
#                 newlist.append(activity.val())
#         else:
#             if activity.val()["long"] == lengthSwitchStatus:
#                 newlist.append(activity.val())
#     randActivity = random.choice(newlist)
#     _data = randActivity["type"] + ": " + randActivity["desc"]
#     yield f"id: 1\ndata: {_data}\nevent: newactivity\n\n"
#     sleep(5)
# sleep(0.075)

# activitiesDatabase = firedb.child("activities").get()
#         newlist = []
#         for activity in activitiesDatabase.each():
#             newlist.append(activity.val())
#         while True:
#             phoneSwitchStatus = phoneSwitch.value
#             if phoneSwitchStatus == 1:
#                 randActivity = random.choice(newlist)
#                 global activityString
#                 activityString = randActivity["type"] + ": " + randActivity["desc"]                 
#                 yield f"id: 1\ndata: {activityString}\nevent: online\n\n"