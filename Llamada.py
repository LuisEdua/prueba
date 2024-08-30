import requests
import json
import datetime
import pytz
import matplotlib.pyplot as plt
import numpy as np

# Solicitar al usuario el nombre del mercado
market = input("Enter a market name: ")
period, f, t = "", "", ""

payload = {}

def preguntar():
    period = input("Enter a period: ")
    if not period:
        f = input("From date: ")
        t = input("To date: ")
        if not f or not t:
            print("Please enter valid dates")
            preguntar()
        else:
            payload["time_from"] = f
            payload["time_to"] = t
    else:
        payload["period"] = period

preguntar()

# Construir la URL de la API
url = f'https://app.aion.com.mx/api/v2/peatio/public/markets/{market}/k-line'

# Realizar la solicitud GET a la API
response = requests.get(url, data=payload)
r_json = json.loads(response.text)

print(r_json)

# Convertir el timestamp a la zona horaria 'America/Mexico_City'
timezone = pytz.timezone('America/Mexico_City')
for arr in r_json:
    timestamp = arr[0]
    time = datetime.datetime.fromtimestamp(timestamp, tz=pytz.utc)
    local_time = time.astimezone(timezone)
    arr[0] = local_time.strftime('%Y-%m-%d %H:%M:%S')

print(r_json)

# Extraer los datos para graficar
times = [arr[0] for arr in r_json]
open_prices = [arr[1] for arr in r_json]
high_prices = [arr[2] for arr in r_json]
low_prices = [arr[3] for arr in r_json]
close_prices = [arr[4] for arr in r_json]

# Crear un arreglo para el eje X (índices de tiempo)
x_arr = np.arange(1, len(r_json) + 1)

# Crear y personalizar la figura
plt.figure(figsize=(10, 5))
plt.plot(x_arr, open_prices, label='Apertura')
plt.plot(x_arr, high_prices, label='Alto')
plt.plot(x_arr, low_prices, label='Bajo')
plt.plot(x_arr, close_prices, label='Cierre')

# Etiquetas y título del gráfico
plt.xlabel('Time')
plt.ylabel('Precio')
plt.title(f'Precio del mercado: {market}')
plt.xticks(ticks=x_arr, labels=times, rotation=45, ha='right')
plt.legend()
plt.tight_layout()

# Mostrar el gráfico
plt.show()
