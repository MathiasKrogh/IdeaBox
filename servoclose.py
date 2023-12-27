from turtle import right
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory(host='192.168.219.87')



# Min and Max pulse widths converted into milliseconds
# To increase range of movement:
#   increase maxPW from default of 2.0
#   decrease minPW from default of 1.0
# Change myCorrection using increments of 0.05 and
# check the value works with your servo.
myCorrection=0.45
maxPW=(2.0+myCorrection)/1000
minPW=(2.0-myCorrection)/1000

leftServo = Servo("GPIO5",min_pulse_width=minPW,max_pulse_width=maxPW,pin_factory=factory)
rightServo = Servo("GPIO12",min_pulse_width=minPW,max_pulse_width=maxPW,pin_factory=factory)

print("Using GPIO5 and GPIO12")
print("Max pulse width is set to 2.45 ms")
print("Min pulse width is set to 0.55 ms")

leftServo.mid()
rightServo.mid()
print("Set to middle position")
sleep(1)