import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage, ttk
import sqlite3
import pandas as pd

# Funkcja do rejestracji użytkownika w bazie danych
def register_user_to_db(username, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Rejestracja", "Rejestracja zakończona sukcesem!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Błąd rejestracji", "Nazwa użytkownika już istnieje")

# Funkcja do tworzenia bazy danych
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

create_db()

# Funkcja do centrowania okna na ekranie
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')

# Funkcja logowania użytkownika
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    result = c.fetchone()
    conn.close()
    
    if result:
        login_window.destroy()
        show_load_xls_window()
    else:
        messagebox.showerror("Błąd logowania", "Nieprawidłowa nazwa użytkownika lub hasło")

def load_xls_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls *.xlsx")])
    if file_path:
        data = pd.read_excel(file_path)
        data.dropna(axis=1, how='all', inplace=True)
        
        # Przenieś wartości "Naczepa" z kolumny "Kierowca" do kolumny "Unnamed: 1" i usuń zbędne dane
        for i, row in data.iterrows():
            if pd.notna(row['Kierowca']) and 'Naczepa' in row['Kierowca']:
                naczepa_info = row['Kierowca']
                naczepa_cleaned = naczepa_info.split(' (')[0] if ' (' in naczepa_info else naczepa_info
                data.at[i, 'Unnamed: 1'] = naczepa_cleaned
                data.at[i, 'Kierowca'] = None
        
        # Przenieś wartości "Przewoźnik" z kolumny "Unnamed: 1" do kolumny "Unnamed: 0" i usuń zbędne dane
        for i, row in data.iterrows():
            if pd.notna(row['Unnamed: 1']) and 'Przewoźnik' in row['Unnamed: 1']:
                przewoznik_info = row['Unnamed: 1']
                przewoznik_cleaned = przewoznik_info.split(' (')[0] if ' (' in przewoznik_info else przewoznik_info
                data.at[i, 'Unnamed: 0'] = przewoznik_cleaned
                data.at[i, 'Unnamed: 1'] = None
    
    data = data.fillna('')
    data = data.replace({None: ''})
    data['Data'] = data['Data'].apply(lambda x: '' if pd.isna(x) else x)

                
    xls_window.destroy()
    show_main_window(data)

# Funkcja do wyświetlenia okna do wczytania pliku XLS
def show_load_xls_window():
    global xls_window

    xls_window = tk.Tk()
    xls_window.iconbitmap('pngs/favicon.ico')
    xls_window.title("Wgraj rozpiske")
    center_window(xls_window, 400, 200)

    tk.Label(xls_window, text="Proszę wgrać plik Rozpiski", font=('Arial', 14)).pack(pady=20)
    tk.Button(xls_window, text="Wgraj plik", command=load_xls_file, font=('Arial', 12)).pack(pady=20)

    xls_window.mainloop()

# Funkcja do wyświetlenia głównego okna
def show_main_window(data):
    root = tk.Tk()
    root.title("Rozpiska")
    root.iconbitmap('pngs/favicon.ico')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}')
    center_window(root, screen_width, screen_height)

    # Dodanie Treeview do wyświetlania danych
    tree = ttk.Treeview(root)
    tree.pack(expand=True, fill='both')

    # Definiowanie kolumn
    columns = ["Przewoźnik", "Naczepa", "Kierowca", "Telefon", "Ciągnik", "Data", "Godzina", "Numer Trasy", "Trasa", "Koniec", "Kilometry"]
    tree["columns"] = columns

    # Ustawienie nagłówków kolumn
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    # Dodanie danych do Treeview
    for index, row in data.iterrows():
        tree.insert("", "end", values=list(row))

    root.mainloop()

# Funkcja do wyświetlenia okna rejestracji
def show_register_window():
    register_window = tk.Toplevel(login_window)
    register_window.title("Rejestracja")
    center_window(register_window, 400, 300)
    
    tk.Label(register_window, text="Nazwa użytkownika", font=('Arial', 14)).pack(pady=10)
    entry_new_username = tk.Entry(register_window, font=('Arial', 14))
    entry_new_username.pack(pady=5)
    
    tk.Label(register_window, text="Hasło", font=('Arial', 14)).pack(pady=10)
    entry_new_password = tk.Entry(register_window, font=('Arial', 14), show='*')
    entry_new_password.pack(pady=5)
    
    def register():
        username = entry_new_username.get()
        password = entry_new_password.get()
        register_user_to_db(username, password)
        register_window.destroy()

    # Dodajemy przycisk "Zarejestruj"
    tk.Button(register_window, text="Zarejestruj", command=register, font=('Arial', 12)).pack(pady=20)

# Funkcja do wyświetlenia okna logowania
def show_login_window():
    global login_window, entry_username, entry_password, background_image

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

    button_register = tk.Button(login_window, text="Zarejestruj", command=show_register_window, font=('Arial', 12))
    button_register.place(relx=0.5, rely=0.71, anchor='center')

    login_window.mainloop()

# Główne wywołanie funkcji do wyświetlenia okna logowania
show_login_window()
