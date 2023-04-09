import board
import busio
import digitalio
import time

# Define GPIO pins for motor control
motor_enable = digitalio.DigitalInOut(board.A1)
motor_enable.direction = digitalio.Direction.OUTPUT
motor_in1 = digitalio.DigitalInOut(board.A2)
motor_in1.direction = digitalio.Direction.OUTPUT
motor_in2 = digitalio.DigitalInOut(board.A3)
motor_in2.direction = digitalio.Direction.OUTPUT

# Enable the motor
motor_enable.value = True

while True:
    # Vary power from 0 to 100% in 5 sec
    for i in range(101):
        power = i / 100.0
        motor_in1.value = True
        motor_in2.value = False
        motor_enable.value = power
        print("Puissance du moteur :", power)
        time.sleep(0.05)

    # Vary power from 100% to -100% in 10 sec
    for i in range(201):
        if i < 101:
            power = 1.0 - (i / 100.0)
        else:
            power = (i - 100) / -100.0
        motor_in1.value = power >= 0
        motor_in2.value = power < 0
        motor_enable.value = abs(power)
        print("Puissance du moteur :", power)
        time.sleep(0.05)

    # Vary power from -100% to 0% in 5 sec
    for i in range(101):
        power = (100 - i) / 100.0
        motor_in1.value = False
        motor_in2.value = True
        motor_enable.value = power
        print("Puissance du moteur :", power)
        time.sleep(0.05)
