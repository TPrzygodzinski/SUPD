import tkinter as tk
from tkinter import messagebox, PhotoImage
import requests
import ctypes
import folium
from tkinterweb import HtmlFrame

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')

def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == 'admin' and password == 'haslo':
        login_window.destroy()
        show_main_window()
    else:
        messagebox.showerror("Błąd logowania", "Nieprawidłowa nazwa użytkownika lub hasło")

def show_main_window():
    root = tk.Tk()
    root.title("Geokodowanie adresu")
    root.iconbitmap('pngs/favicon.ico')
    
    # Ustawienie rozmiaru okna i wycentrowanie go
    width = 600  # Przykładowa szerokość okna
    height = 300  # Przykładowa wysokość okna
    center_window(root, width, height)

    entry_address = tk.Entry(root, font=('Arial', 14), width=50)
    entry_address.pack(pady=20)
    
    fetch_button = tk.Button(root, text="Pobierz współrzędne", command=lambda: fetch_coordinates(entry_address.get(), result_label), font=('Arial', 12))
    fetch_button.pack(pady=10)
    
    result_label = tk.Label(root, text="Wprowadź adres i kliknij przycisk.", font=('Arial', 12))
    result_label.pack(pady=20)
    
    root.mainloop()


def fetch_coordinates(address, label):
    if not address:
        messagebox.showinfo("Błąd", "Proszę wprowadzić adres.")
        return
    URL_maps = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': 'AIzaSyDGvI8Ove0W6nSL6a1EZmsSL7Q5JqkoGRA', 'language': 'pl', 'region': 'pl'}
    response = requests.get(URL_maps, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            latitude = data['results'][0]['geometry']['location']['lat']
            longitude = data['results'][0]['geometry']['location']['lng']
            label.config(text=f"Szerokość: {latitude}, Długość: {longitude}")
        else:
            label.config(text="Nie znaleziono lokalizacji.")
    else:
        label.config(text="Błąd podczas żądania geokodowania.")
    
    
    
# Okno logowania
login_window = tk.Tk()
login_window.title("SUPD / GFL")
login_window.iconbitmap('pngs/favicon.ico')
center_window(login_window, 600, 300)

background_image = PhotoImage(file='pngs/gfl.png')
background_label = tk.Label(login_window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

entry_username = tk.Entry(login_window, font=('Arial', 14))
entry_username.place(relx=0.5, rely=0.4, anchor='center')
entry_username.insert(0, "admin")

entry_password = tk.Entry(login_window, font=('Arial', 14), show='*')
entry_password.place(relx=0.5, rely=0.5, anchor='center')
entry_password.insert(0, "haslo")

button_login = tk.Button(login_window, text="Zaloguj", command=login, font=('Arial', 12))
button_login.place(relx=0.5, rely=0.61, anchor='center')

login_window.mainloop()