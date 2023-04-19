import time
import board
from adafruit_tca8418 import TCA8418

i2c = board.I2C()  # utilise board.SCL et board.SDA
# i2c = board.STEMMA_I2C()  # Pour utiliser le connecteur STEMMA QT intégré sur un microcontrôleur
tca = TCA8418(i2c)

# define the key mapping
keymap = (
    ("D", "B", "C", "A"),
    ("#", "6", "9", "3"),
    ("0", "5", "8", "2"),
    ("*", "4", "7", "1")
)

# define the keypad pins
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

# set up the keypad pins
for pin in KEYPADPINS:
    tca.keypad_mode[pin] = True
    tca.enable_int[pin] = True
    tca.event_mode_fifo[pin] = True

# enable the INT output pin
tca.key_intenable = True

while True:
    if tca.key_int:
        # figure out how big the queue is
        events = tca.events_count
        # loop through the events and print them out
        for _ in range(events):
            keyevent = tca.next_event
            event = keyevent & 0x7F
            event -= 1
            row = event // 10
            col = event % 10
            if keyevent & 0x80:
                print("Key down")
            else:
                print("Key up")
            print("Row %d, Column %d, Key %s" % (row, col, keymap[row][col]))
        tca.key_int = True
        time.sleep(0.01)
