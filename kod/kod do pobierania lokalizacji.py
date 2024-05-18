import requests

# Ustawienie URL usługi geokodowania i klucza API
URL_maps = 'https://maps.googleapis.com/maps/api/geocode/json'
params = {
    'address': 'Trzcińska 26/9 96-100 Skierniewice',
    'key': 'AIzaSyDGvI8Ove0W6nSL6a1EZmsSL7Q5JqkoGRA',
    'language': 'pl',
    'region':'pl'
}

# Wykonywanie zapytania GET z użyciem parametrów
odpowiedz_google_maps = requests.get(URL_maps, params=params)

if odpowiedz_google_maps.status_code == 200:
    data = odpowiedz_google_maps.json()  # Odczytanie odpowiedzi JSON
    print(data)

szerokosc = odpowiedz_google_maps.json()['results'][0]['geometry']['location']['lat']
dlugosc = odpowiedz_google_maps.json()['results'][0]['geometry']['location']['lng']



print(f"Szerokość i długość geograficzna: {szerokosc} {dlugosc}")

