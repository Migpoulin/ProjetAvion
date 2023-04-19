import keypad
import board
import time

bouttons_clavier = {
    0: "1",
    1: "2",
    2: "3",
    3: "A",
    4: "4",
    5: "5",
    6: "6",
    7: "B",
    8: "7",
    9: "8",
    10: "9",
    11: "C",
    12: "*",
    13: "0",
    14: "#",
    15: "D",
}

km = keypad.KeyMatrix(
    row_pins=(board.A0, board.A1, board.A2, board.A3),
    column_pins=(board.D13, board.D12, board.D11,board.D10),
)

liste_nombre = []  
key_pressed = False  

while True:
    event = km.events.get()
    if event:
        if not key_pressed:
            key_number = event.key_number
            boutton_clavier = bouttons_clavier.get(key_number)
            if boutton_clavier == "#":
                nombre = int("".join(liste_nombre))
                nombreCarre = nombre ** 2
                print(nombreCarre)
                liste_nombre = []  
            elif boutton_clavier.isdigit():
                liste_nombre.append(boutton_clavier)
                print("".join(liste_nombre))
            key_pressed = True  
    else:
        key_pressed = False  
    time.sleep(0.2)  
