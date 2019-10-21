import RPi.GPIO as GPIO
import time
import tsl2591
from gpiozero import MCP3008

while True:
	tsl = tsl2591.Tsl2591()
	full, ir = tsl.get_full_luminosity()
	l = tsl.calculate_lux(full, ir)
	lux=round(l)
	print("La intensidad luminica es: ", lux)
	print("--------------------------------------------------")
	time.sleep(1)
	t = MCP3008(channel=0, device=0)
	temperature=(t.value*3.3)*100
	temperature= round (temperature-5)
	print("La temperatura es: ", temperature)
	print("--------------------------------------------------")
	time.sleep(1)
	h = MCP3008(channel=1, device=0)
	moisture = (h.value*10)
	print("La humedad es:", moisture)
	print("--------------------------------------------------")
	time.sleep(1)
