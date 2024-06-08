from tkinter import *

root = Tk()

e = Entry(root, fg="blue", bg="#87cefa", width=20)
e.grid(row=0, column=1)
e.insert(0, "witaj w aplikacji")


def cosiestanie():
    witam = e.get()
    mylabel3 = Label(root, text=witam)
    mylabel3.grid(row = 3, column = 1)


mybutton = Button(root, text = "klilnij!", padx = 50, pady = 50, command=cosiestanie, fg="blue", bg="#87cefa")

mylabel1 = Label(root, text="hello world")
mylabel2 = Label(root, text="GFL kofam")

mybutton.grid(row = 1, column = 1)

mylabel1.grid(row = 0, column = 0)
mylabel2.grid(row = 0, column = 2)

root.mainloop()