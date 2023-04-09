import time
import board
import adafruit_hcsr04
import neopixel

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A0, echo_pin=board.A1)
led = neopixel.NeoPixel(board.NEOPIXEL, 1)

while True:
    try:
        distance = sonar.distance
        if distance > 15:
            led.fill((0, 255, 0))
        elif distance <= 15 and distance >= 5:
            led.fill((255, 255, 0)) 
        else:
            led.fill((255, 0, 0)) 
        print(distance)
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.1)
