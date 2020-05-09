import RPi.GPIO as GPIO
import time
import tsl2591
import mysql.connector
import threading
from gpiozero import MCP3008


mydb = mysql.connector.connect(
        host = '192.168.0.12',
        database = 'db',
        port = '3306',
        user = 'user',
        password = 'password'
        )

def temperatureActuator():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT)
    GPIO.output(23, GPIO.HIGH)
    return


def moistureActuator():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(20, GPIO.HIGH)        
    return


def luxActuator():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)        
    return


def getPlantInfo():
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
    plantTemperature, plantMoisture, plantLux = getPlantInfo()
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
        print("Es necesario riego")
        moistureActuator()
    elif moisture > plantMoisture:
        print("Humedad demasiado alta")
    else:
        print("Humedad adecuada")
    if temperature > plantTemperature:
        print("Temperatura demasiado alta")
        temperatureActuator()
    elif temperature < plantTemperature:
        print("Temperatura demasiado baja")
    else:
        print("Temperatura adecuada")   
    if lux > plantLux:
        print("Intensidad luminica demasiado alta")
    elif lux < plantLux:
        print("Intensidad luminica demasidado baja")
    else:
        print("Intensidad luminica adecuada")
    postSensorInfo(moisture, lux, temperature)





