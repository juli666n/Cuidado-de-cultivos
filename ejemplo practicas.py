import RPi.GPIO as GPIO
import time
import tsl2591
import mysql.connector
import threading
from gpiozero import MCP3008


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)


mydb = mysql.connector.connect(
        host = '192.168.0.14',
        database = 'db',
        port = '3306',
        user = 'user',
        password = 'password'
        )


def activateTemperatureActuator():
    GPIO.output(17, 1)
    print("AT")
    return


def deactivateTemperatureActuator():
    GPIO.output(17, 0)
    print("DT")
    return


def activateMoistureActuator():
    GPIO.output(27, 1)        
    print("AM")
    return


def deactivateMoistureActuator():
    GPIO.output(27, 0)        
    print("DM")
    return


def activateLuxActuator():
    GPIO.output(22, 1)        
    print("AL")
    return


def deactivateLuxActuator():
    GPIO.output(22, 0)        
    print("DL")
    return

def getPlantInfo(plantTemperature, plantMoisture, plantLux):
    mydb.connect()
    mycursor = mydb.cursor()
    query = "SELECT temperature, moisture, lux FROM miHuertaSite_plant WHERE isSelected = '1'" 
    mycursor.execute(query)
    values = mycursor.fetchone()
    try:
        plantTemperature, plantMoisture, plantLux = values
        mycursor.close()
        mydb.close()
    except:
        pass
    return plantTemperature, plantMoisture, plantLux


def postSensorInfo(temperature, lux, moisture):
    mydb.connect()
    mycursor = mydb.cursor()
    updateSensors = "UPDATE miHuertaSite_sensor SET temperatureSensor = %s, luxSensor = %s, moistureSensor = %s WHERE id = '1'" 
    mycursor.execute(updateSensors, (temperature, lux, moisture))
    mydb.commit()
    mycursor.close()
    mydb.close()

while True:
    plantTemperature, plantMoisture, plantLux = getPlantInfo(0, 0, 0)
    tsl = tsl2591.Tsl2591()
    full, ir = tsl.get_full_luminosity()
    l = tsl.calculate_lux(full, ir)
    lux=round(l)
    t = MCP3008(channel=0, device=0)
    temperature=(t.value*3.3)*100
    temperature= round (temperature-5)
    h = MCP3008(channel=1, device=0)
    moisture = (h.value*10)
    print("Humedad = ", moisture)
    print("Intensidad luminica = ", lux)
    print("Temperatura = ", temperature)
    if moisture < plantMoisture:
       deactivateMoistureActuator()
    elif moisture > plantMoisture:
        activateMoistureActuator()
    if temperature > plantTemperature:
        activateTemperatureActuator()
    elif temperature < plantTemperature:
        deactivateTemperatureActuator()
    if lux > plantLux:
        deactivateLuxActuator()
    elif lux < plantLux:
        activateLuxActuator()
    postSensorInfo(temperature, lux, moisture)





