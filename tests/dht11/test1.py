import time
import adafruit_dht
import board

dht_pin = board.A1
dht_device = adafruit_dht.DHT11(dht_pin)


tabTemperature = []
tabHumidite = []

while True:
    temperature = dht_device.temperature
    humidity = dht_device.humidity
        
    tabTemperature.append(temperature)
    tabHumidite.append(humidity)

    if len(tabTemperature) > 10:
        tabTemperature.pop(0)
    if len(tabHumidite) > 10:
        tabHumidite.pop(0)

    print('Temperature: {}, Humidite: {}'.format(temperature, humidity))

    moyTemperature = sum(tabTemperature) / len(tabTemperature)
    moyHumidite = sum(tabHumidite) / len(tabHumidite)

    print('Moyenne de temperature: {}, Moyenne humidite: {}'.format(moyTemperature, moyHumidite))

    time.sleep(1)
