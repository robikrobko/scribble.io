import random
import tkinter
from tkinter import Tk, Frame, Canvas, CENTER, Button, NW, Label, SOLID
from tkinter import colorchooser, filedialog, OptionMenu, messagebox
from tkinter import DOTBOX, StringVar, simpledialog

import os
import pickle

########### Window Settings ###########

root = Tk()

root.title("Paint - ECTS v1.0")
root.geometry("1100x650")

root.resizable(False, False)

########### Functions ###########

# Variables
prevPoint = [0, 0]
currentPoint = [0, 0]

penColor = "black"
stroke = 1

canvas_data = []

slovicka = ["slnko", "dom", "mrak", "cestoviny", "jablko", "kava", "stol", "clovek", "python", "programator", "server", "caj"]
generator = random.choice(slovicka)


tkinter.messagebox.showinfo(title="Kreslenie", message="Tvoje slovicko je:" +" " + generator)


# Increase Stroke Size By 1
def strokeI():
    global stroke

    if stroke != 10:
        stroke += 1

    else:
        stroke = stroke


# Decrease Stroke Size By 1
def strokeD():
    global stroke

    if stroke != 1:
        stroke -= 1

    else:
        stroke = stroke


def strokeDf():
    global stroke
    stroke = 1


# Pencil
def pencil():
    global penColor

    penColor = "black"


# Eraser
def eraser():
    global penColor

    penColor = "white"


# Pencil Choose Color
def colorChoice():
    global penColor

    color = colorchooser.askcolor(title="Select a Color")


    if color[1]:
        penColor = color[1]

    else:
        pass


# Shape Color Chooser


# Paint Function
def paint(event):
    global prevPoint
    global currentPoint

    x = event.x
    y = event.y

    currentPoint = [x, y]

    if prevPoint != [0, 0]:
        canvas.create_polygon(
            prevPoint[0],
            prevPoint[1],
            currentPoint[0],
            currentPoint[1],
            fill=penColor,
            outline=penColor,
            width=stroke,
        )

    prevPoint = currentPoint

    if event.type == "5":
        prevPoint = [0, 0]


# Close App
def newApp():
    os.startfile("paint.py")


# Clear Screen
def clearScreen():
    canvas.delete("all")


# Main Frame
frame1 = Frame(root, height=150, width=1100)
frame1.grid(row=0, column=0)

# Holder Frame
holder = Frame(frame1, height=120, width=1000, bg="white", padx=6, pady=10)
holder.grid(row=0, column=0, sticky=NW)
holder.place(relx=0.5, rely=0.5, anchor=CENTER)

holder.columnconfigure(0, minsize=120)
holder.columnconfigure(1, minsize=120)
holder.columnconfigure(2, minsize=120)



holder.rowconfigure(0, minsize=30)

#### Tools ####

# Label for Tool 1,2,3
label123 = Label(holder, text="TOOLS", borderwidth=1, relief=SOLID, width=15)
label123.grid(row=0, column=0)

# Tool 1 - Pencil
pencilButton = Button(holder, text="Pencil", height=1, width=12, command=pencil)
pencilButton.grid(row=1, column=0)

# Tool 2 - Eraser
eraserButton = Button(holder, text="Eraser", height=1, width=12, command=eraser)
eraserButton.grid(row=2, column=0)

# Tool 3 - Color Change
colorButton = Button(
    holder, text="Select Color", height=1, width=12, command=colorChoice
)
colorButton.grid(row=3, column=0)

#### FILE ACTIONS ####

# Label for Tool 4,5,6

#### OTHER ####

# Label for Tool 7 and 8
label7 = Label(holder, text="OTHER", borderwidth=1, relief=SOLID, width=15)
label7.grid(row=0, column=1)

# Tool 7 - Clear Screen
clearButton = Button(holder, text="CLEAR", height=1, width=12, command=clearScreen)
clearButton.grid(row=1, column=1)

# Tool 8 - Exit App
exitButton = Button(
    holder, text="Exit", height=1, width=12, command=lambda: root.destroy()
)
exitButton.grid(row=2, column=1)

#### Stroke Size ####

# Label for Tool 8, 9 and 10
label8910 = Label(holder, text="STROKE SIZE", borderwidth=1, relief=SOLID, width=15)
label8910.grid(row=0, column=2)

# Tool 8 - Increament by 1
sizeiButton = Button(holder, text="Increase", height=1, width=12, command=strokeI)
sizeiButton.grid(row=1, column=2)

# Tool 9 - Decreament by 1
sizedButton = Button(holder, text="Decrease", height=1, width=12, command=strokeD)
sizedButton.grid(row=2, column=2)

# Tool 10 - Default
defaultButton = Button(holder, text="Default", height=1, width=12, command=strokeDf)
defaultButton.grid(row=3, column=2)

#### Shapes ####

# Label for Tool 11,12,13


#### Canvas Frame ####

# Main Frame
frame2 = Frame(root, height=500, width=1100)
frame2.grid(row=1, column=0)

# Making a Canvas
canvas = Canvas(frame2, height=450, width=1000, bg="white")
canvas.grid(row=0, column=0)
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


# Event Binding
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", paint)
canvas.bind("<Button-1>", paint)

########### Main Loop ###########

root.mainloop()