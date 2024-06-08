import matplotlib.pyplot as plt

# Dane: listy wartości x i y
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# Tworzenie wykresu punktowego
plt.scatter(x, y, color='red')  # Możesz zmieniać kolor punktów

# Dodawanie tytułu i etykiet osi
plt.title('Wykres punktowy')
plt.xlabel('x')
plt.ylabel('y')

# Opcjonalnie: dodawanie siatki
plt.grid(True)

# Wyświetlanie wykresu
plt.show()
