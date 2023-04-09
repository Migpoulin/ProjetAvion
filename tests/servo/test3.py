import time
import board
import pwmio
from adafruit_motor import servo
import analogio

potentiometer = analogio.AnalogIn(board.A1)

pwm = pwmio.PWMOut(board.A0, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

while True:
    pot_value = potentiometer.value
    angle = int((pot_value - 436) / (51613 - 436) * 180)
    my_servo.angle = angle
    time.sleep(0.01)