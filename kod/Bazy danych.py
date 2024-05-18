import sqlite3

# Połączenie z bazą danych (lub jej utworzenie, jeśli nie istnieje)
conn = sqlite3.connect('przykladowa_baza.db')
c = conn.cursor()

# Tworzenie tabeli
c.execute('''
CREATE TABLE IF NOT EXISTS pracownicy (
    id INTEGER PRIMARY KEY,
    imie TEXT,
    stanowisko TEXT,
    pensja REAL
)
''')
# Wstawianie danych do tabeli
c.execute("INSERT INTO pracownicy (imie, stanowisko, pensja) VALUES ('Jan', 'Dyspozytor', 3200.50)")
c.execute("INSERT INTO pracownicy (imie, stanowisko, pensja) VALUES ('Karol', 'Dyspozytor', 3300.50)")

c.execute("DELETE FROM pracownicy WHERE pensja <= ?", (3200.50,))

# Zapytanie o dane
c.execute("SELECT * FROM pracownicy")
wyniki = c.fetchall()
for wynik in wyniki:
    print(wynik)

conn.commit()

