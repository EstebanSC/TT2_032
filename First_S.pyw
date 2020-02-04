import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 

import os

root=tk.Tk()

FrameP=tk.Canvas(root, height=500,width=700,bg="#f6f2f2")
FrameP.pack()

FrameS=tk.Frame(root,bg="white")
FrameS.place(relx=0.1,rely=0.1)
current_path = os.path.dirname(__file__) # Where your .py file is located
rel_path="Interfaces/"
abs_file_path=os.path.join(current_path,rel_path)
#resource_path = os.path.join(current_path, 'TT2_032') # The resource folder path
#image_path = os.path.join(resource_path, 'Interfaces') # The image folder path
current_file="add.png"
#load= Image.open(abs_file_path+current_file)
#photo=ImageTk.PhotoImage(load)
photo=PhotoImage(file=abs_file_path+current_file)
#photo_bu=photo.
photo_bu=photo.subsample(9,9)
openFile=tk.Button(FrameS, image=photo_bu)
openFile.pack()

root.mainloop()