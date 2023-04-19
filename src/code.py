import time
import board
import pwmio
import busio
import digitalio
import analogio
import math
from adafruit_motor import servo
import mfrc522
from adafruit_tca8418 import TCA8418
import neopixel
import adafruit_dht
import adafruit_hcsr04


#servo
pwm = pwmio.PWMOut(board.A2, frequency=50)
my_servo = servo.Servo(pwm, min_pulse = 500, max_pulse = 2600)
#moteur
motor_enable = digitalio.DigitalInOut(board.A3)
motor_enable.direction = digitalio.Direction.OUTPUT
motor_in1 = digitalio.DigitalInOut(board.RX)
motor_in1.direction = digitalio.Direction.OUTPUT
motor_in2 = digitalio.DigitalInOut(board.TX)
motor_in2.direction = digitalio.Direction.OUTPUT

switch_pin = board.D12
switch = digitalio.DigitalInOut(switch_pin)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

switch_state = switch.value

led = neopixel.NeoPixel(board.NEOPIXEL, 1)

#joystick
x_pin = board.D10
y_pin = board.D9

xVal = analogio.AnalogIn(x_pin)
yVal = analogio.AnalogIn(y_pin)

joystick_button = digitalio.DigitalInOut(board.D6)
joystick_button.direction = digitalio.Direction.INPUT
joystick_button.pull = digitalio.Pull.UP

dht_pin = board.A4
dht_device = adafruit_dht.DHT11(dht_pin)

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A0, echo_pin=board.A1)

#rdr = mfrc522.MFRC522(board.D12, board.D11, board.D13, board.A2, board.D10)
#rdr.set_antenna_gain(0x07 << 4)

i2c = board.I2C()

tca = TCA8418(i2c)
aeroports = {
    101: "YUL Montreal",
    111: "ATL Atlanta",
    222: "HND Tokyo",
    764: "LHR London",
    492: "CAN Baiyun",
    174: "CDG Paris",
    523: "AMS Amsterdam"

}

keymap = (
    ("D", "B", "C", "A"),
    ("#", "6", "9", "3"),
    ("0", "5", "8", "2"),
    ("*", "4", "7", "1")
)

KEYPADPINS = (
    TCA8418.R0,
    TCA8418.R1,
    TCA8418.R2,
    TCA8418.R3,
    TCA8418.C0,
    TCA8418.C1,
    TCA8418.C2,
    TCA8418.C3,
    )
for pin in KEYPADPINS:
    tca.keypad_mode[pin] = True
    tca.enable_int[pin] = True
    tca.event_mode_fifo[pin] = True

tca.key_intenable = True


# Définition des états
def etat_initial():
    led.fill((255, 0, 0))  
    # Actions à effectuer lors de l'entrée dans l'état initial
    
    #do_read()
    print("En attente d'une carte rfid")
    #while True:
        # Check if a card has been read
        #(stat, tag_type) = rdr.request(rdr.REQIDL)
        #if stat == rdr.OK:
            #(stat, raw_uid) = rdr.anticoll()
            #if stat == rdr.OK:
                #print("New card detected")
                #print("  - tag type: 0x%02x" % tag_type)
                #print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                #print('')
                # Transition to state 2
                #return etat_2()
        
        #time.sleep(0.1)
    time.sleep(4)
    return etat_2
    
def etat_2():
    led.fill((255, 255, 0))
    global aeroport_selectionne
    aeroport_selectionne = ""
    
    
    

    while True:
        
        
        user_input = ""
        user_started = False
        print("Entrer votre code de vol : ")
        while len(user_input) < 3 or not user_started:
            if tca.key_int:
                events = tca.events_count
                for _ in range(events):
                    keyevent = tca.next_event
                    event = keyevent & 0x7F
                    event -= 1
                    row = event // 10
                    col = event % 10
                    if keyevent & 0x80:
                        if not user_started and keymap[row][col] == "#":
                            user_started = True
                            print("#", end="")
                        elif user_started and len(user_input) < 3 and keymap[row][col].isdigit():
                            user_input += keymap[row][col]
                            print(keymap[row][col], end="")
                tca.key_int = True
                time.sleep(0.01)
            time.sleep(0.1)

        print("\nUser input:", user_input)
        if int(user_input) in aeroports.keys():
            aeroport_selectionne = aeroports[int(user_input)]
            print("Code valide, il est possible de demarrer en activant l'interupteur:")
        else:
            print("Code invalide. Veuillez réessayer.")
            continue
    
        while True:
            if switch.value:
                print("Interrupteur on, passage a l'etat 3")
                time.sleep(1)
                return etat_3
                
            else:
                pass
def etat_3():
    led.fill((0, 255, 0))
    
    temperature = dht_device.temperature
    humidity = dht_device.humidity
    
    angle_lock = False
    power_lock = False
    locked_angle = 0
    locked_power = 0
    
    while True:
        
        x = xVal.value - 32768
        y = yVal.value - 32768

        angleJoystick = int((x + 32768) / 65535 * 180)
        my_servo.angle = angleJoystick
        power = int((y + 32768) / 65535 * 100)
        
        try:
            distance = sonar.distance
            if distance < 10:
                my_servo.angle = 0
                motor_enable.value = 0
                motor_in1.value = True
                motor_in2.value = True
                return etat_initial()
           
        except RuntimeError:
            pass
        
        if not joystick_button.value:
            if not angle_lock:
                angle_lock = True
                locked_angle = my_servo.angle
                print("Angle verrouillé : {}".format(locked_angle))
            else:
                angle_lock = False
                locked_angle = 0
                print("Angle déverrouillé")
        

        if not joystick_button.value:
            if not power_lock:
                power_lock = True
                locked_power = power
                print("Puissance verrouillée : {}".format(locked_power))
            else:
                power_lock = False
                locked_power = 0  
                print("Puissance déverrouillée")
        
        if angle_lock:
            my_servo.angle = locked_angle
        
        if power_lock:
            power = locked_power
            
        
        if switch.value:
            pass
                
        else:
            print("Interrupteur off, passage a l'etat initial")
            time.sleep(1)
            return etat_initial
        
                
        
        print(f"Puissance: {power if not locked_power else locked_power} Angle Servo: {my_servo.angle if not locked_angle else locked_angle}  Destination  {aeroport_selectionne} - Humidité: {humidity}  Température: {temperature}  ")
        
        motor_in1.value = power >= 0
        motor_in2.value = power < 0
        motor_enable.value = abs(power)
        if abs(power) < 10:
            motor_enable.value = 0
            motor_in1.value = True
            motor_in2.value = True
        else:
            motor_enable.value = abs(power)
            motor_in1.value = power >= 0
            motor_in2.value = power < 0
        
        time.sleep(0.1)
# Boucle principale
def boucle_principale():
    # Initialisation de la machine à états finis
    etat_courant = etat_initial()

    while True:
        # Exécution de l'état courant
        etat_courant = etat_courant()

        # Sortie de la boucle si l'état final est atteint
        if etat_courant == None:
            break

# Programme principal
boucle_principale()
