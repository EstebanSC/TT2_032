import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 

import os

root=tk.Tk()

FrameP=tk.Canvas(root, height=500,width=700,bg="#f6f2f2")
FrameP.pack()

#current_path = os.path.dirname(__file__) # Where your .py file is located
#resource_path = os.path.join(current_path, 'TT2_032') # The resource folder path
#image_path = os.path.join(resource_path, 'Interfaces') # The image folder path
#load=pygame.image.load(os.path.join(image_path, 'add.png'))
load= Image.open('/Interfaces/add.png')
photo=ImageTk.PhotoImage(load)
openFile=tk.Button(root,image=photo)
openFile.pack()
root.mainloop()