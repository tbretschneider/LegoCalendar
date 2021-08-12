# trial for creating a tkinter window

#import tkinter as tk
from tkinter import *

root = Tk()

myLabel = Label(root, text = "how many projects are there?")
myLabel.pack()

e = Entry(root, width = 50)
e.pack()
e.insert(0,"")

def myClick():
    projectNum = int(e.get())
    for i in range(projectNum):
        myLabel = Label(root, text = "well done")
        myLabel.pack()

myButton = Button(root, text = "Enter Your Name", command = myClick)
myButton.pack()

myLabel2 = Label(root, text = "Hi there")
myLabel2.pack()

root.mainloop()
