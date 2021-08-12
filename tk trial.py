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
    myLabel = Label(root, text = "what are the projects?")
    myLabel.pack()

    projects = []
    
    for i in range(projectNum):
        e1 = Entry(root, width = 50)
        e1.pack()
        e1.insert(0,"")
        projects.append(e1.get())
    myButton = Button(root, text = "Submit", command = myClick)
    myButton.pack()

    return projects
        
myButton = Button(root, text = "Submit", command = myClick)
myButton.pack()


root.mainloop()

print(projects)
