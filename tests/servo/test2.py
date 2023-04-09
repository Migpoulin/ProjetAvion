import time
import board
import pwmio
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.A0, frequency=50)
my_servo = servo.Servo(pwm, min_pulse = 500, max_pulse = 2600)

while True:
    angle = int(input("Enter an angle (0-180): "))

    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180

    my_servo.angle = angle
    
    time.sleep(0.5)