import time
import math
import board
import analogio

x_pin = board.A0
y_pin = board.A1

xVal = analogio.AnalogIn(x_pin)
yVal = analogio.AnalogIn(y_pin)

while True:
    x = xVal.value - 32768  
    y = yVal.value - 32768  
    coteC = math.sqrt(x ** 2 + y ** 2) 
    if x >= 0:
        angle = math.degrees(math.asin(y / coteC)) 
    else:
        angle = 180 - math.degrees(math.asin(y / coteC)) 
    if angle < 0:
        angle += 360  
    print(angle)
    time.sleep(0.1)
