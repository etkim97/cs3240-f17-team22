import tkinter
from tkinter import *

if __name__ == '__main__':
    top = tkinter.Tk()
    B = tkinter.Button(top, text="Login")
    L1 = Label(top, text="User Name")
    L1.pack()
    E1 = Entry(top, bd=5)
    E1.pack()
    L1 = Label(top, text="Login")
    L1.pack()
    E1 = Entry(top, bd=5)
    E1.pack()
    B.pack()
    top.mainloop()