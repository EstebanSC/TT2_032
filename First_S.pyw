import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 
import os

root=tk.Tk()

FrameP=tk.Canvas(root, height=500,width=700,bg="#f6f2f2")
FrameP.pack()

load= Image.open("Interfaces/add.png")
photo=ImageTk.PhotoImage(load)
openFile=tk.Button(root,image=photo)
openFile.pack()
root.mainloop()