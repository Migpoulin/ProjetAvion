import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd

i2c = busio.I2C(board.SCL, board.SDA)

lcd_address = 0x27

lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, lcd_address)

lcd.message = "Hello, world!"
