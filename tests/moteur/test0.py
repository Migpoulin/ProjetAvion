import board
import busio
import digitalio
import time

# Définissez les broches GPIO pour le contrôle du moteur
motor_enable = digitalio.DigitalInOut(board.A1)
motor_enable.direction = digitalio.Direction.OUTPUT
motor_in1 = digitalio.DigitalInOut(board.A2)
motor_in1.direction = digitalio.Direction.OUTPUT
motor_in2 = digitalio.DigitalInOut(board.A3)
motor_in2.direction = digitalio.Direction.OUTPUT

# Activez le moteur
motor_enable.value = True

# Faites tourner le moteur dans un sens
motor_in1.value = True
motor_in2.value = False
time.sleep(1)

# Faites tourner le moteur dans l'autre sens

motor_in1.value = False
motor_in2.value = True
time.sleep(1)

# Arrêtez le moteur
motor_in1.value = False
motor_in2.value = False

# Désactivez le moteur
motor_enable.value = False