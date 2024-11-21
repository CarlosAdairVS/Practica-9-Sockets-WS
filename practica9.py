import requests
import socket
import json

# Claves API
OPENWEATHER_API_KEY = '86a2c9a61aadd05c335c71b5ebf4331d'
GEONAMES_USERNAME = 'migfel'

# URLs para las APIs REST
OPENWEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
GEONAMES_URL = "http://api.geonames.org/searchJSON"

def get_weather_rest(city):
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',  # para obtener la temperatura en grados Celsius
        'lang': 'es'  # para obtener la descripción en español
    }
    response = requests.get(OPENWEATHER_URL, params=params)
    return response.json()

def get_location_rest(place_name):
    params = {
        'q': place_name,
        'maxRows': 1,
        'username': GEONAMES_USERNAME
    }
    response = requests.get(GEONAMES_URL, params=params)
    return response.json()

def get_weather_socket(city):
    host = 'api.openweathermap.org'
    port = 80
    request_line = f"GET /data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es HTTP/1.1\r\n"
    headers = f"Host: {host}\r\nConnection: close\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request_line.encode() + headers.encode())
        response = s.recv(4096).decode()
        
    return json.loads(response.split("\r\n\r\n")[1])  # Parse the response body as JSON

def get_location_socket(place_name):
    host = 'api.geonames.org'
    port = 80
    request_line = f"GET /searchJSON?q={place_name}&maxRows=1&username={GEONAMES_USERNAME} HTTP/1.1\r\n"
    headers = f"Host: {host}\r\nConnection: close\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request_line.encode() + headers.encode())
        response = s.recv(4096).decode()
        
    return json.loads(response.split("\r\n\r\n")[1])  # Parse the response body as JSON

def display_weather_info(data):
    if 'main' in data:
        print(f"Ciudad: {data['name']}")
        print(f"Temperatura: {data['main']['temp']}°C")
        print(f"Humedad: {data['main']['humidity']}%")
        print(f"Condiciones: {data['weather'][0]['description'].capitalize()}")
    else:
        print("No se pudo obtener la información del clima.")

def display_location_info(data):
    if 'geonames' in data and len(data['geonames']) > 0:
        location = data['geonames'][0]
        print(f"Lugar: {location['name']}")
        print(f"País: {location['countryName']}")
        print(f"Latitud: {location['lat']}")
        print(f"Longitud: {location['lng']}")
    else:
        print("No se pudo obtener la información de la localización.")

def main():
    method = input("¿Con qué método quieres hacer la petición? (rest/socket): ").strip().lower()
    service = input("¿Qué servicio quieres usar? (weather/location): ").strip().lower()
    query = input("Introduce el nombre de la ciudad o lugar: ").strip()

    if service == 'weather':
        if method == 'rest':
            result = get_weather_rest(query)
        elif method == 'socket':
            result = get_weather_socket(query)
        else:
            print("Método no válido")
            return
        display_weather_info(result)
    elif service == 'location':
        if method == 'rest':
            result = get_location_rest(query)
        elif method == 'socket':
            result = get_location_rest(query)
        else:
            print("Método no válido")
            return
        display_location_info(result)
    else:
        print("Servicio no válido")
        return

if __name__ == "__main__":
    main()


