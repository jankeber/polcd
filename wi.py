import time
import Adafruit_CharLCD as LCD
import os
import sqlite3

counter = 0

if not os.path.exists('temperature_baza'):
	conn = sqlite3.connect('temperature_baza')
	conn.execute("CREATE TABLE temperature (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, temperatura REAL NOT NULL)")

conn = sqlite3.connect("temperature_baza")

LCD_RS = 17
LCD_EN = 27
LCD_D4 = 22
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25

LCD_COLUMNS = 20
LCD_ROWS = 4

lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_COLUMNS, LCD_ROWS)

while True:
	tfile = open("/sys/bus/w1/devices/10-00080283986e/w1_slave")
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	temperature_round = round(temperature, 1)
	temperature_str = str(temperature_round)
	
	lcd.clear()
	lcd.message("  Strezniska soba:  \n" + "    " + temperature_str + " stopinj")
	time.sleep(3)
	lcd.clear()
	lcd.message("Vreme zunaj")
	time.sleep(3)
	print counter
	if counter == 3:
		conn.execute("INSERT INTO temperature (temperatura) VALUES (?)", (temperature_round,))
		conn.commit()
		counter = 0
		print "Counter reset"
	counter = counter + 1
