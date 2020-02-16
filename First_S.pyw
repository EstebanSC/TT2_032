import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 

import os

root=tk.Tk()
root.geometry("900x500")
v=tk.StringVar()

def getfile():
    filename=filedialog.askopenfilename(initialdir="/",title="Seleccione Archivo",
    filetypes=(("text","*.txt"),("all files","*.txt")))
    st=filename.text

    v.set(filename)
    
    #Path_F.setvar(filename)
current_path = os.path.dirname(__file__) # Where your .py file is located


FrameP=tk.Canvas(root, height=600,width=1100,bg="white")
FrameP.pack(expand=False)

TituloP=tk.Label(root,text="Sistema para la Prediccion de Actividad Farmacologica",bg="White")
TituloP.config(font=("Arial",26))
TituloP.place(x=30, y=30, in_=root)


rel_path2="Logotipo/"
abs_file_path2=os.path.join(current_path,rel_path2)
current_log="Logotipo.png"
photo_log=PhotoImage(file=abs_file_path2+current_log)
#photo_log.configure(heigth=20, width=30)
pp=photo_log.subsample(5,5)
LogoP=tk.Label(root,height=400, width=400, image=pp,bg="white")
LogoP.place(x=480,y=90,in_=root)

Buscar_A=tk.Label(root,text="Buscar Archivo",bg="White")
Buscar_A.config(font=("Arial",18))
Buscar_A.place(x=180,y=150, in_=root)


#resource_path = os.path.join(current_path, 'TT2_032') # The resource folder path
#image_path = os.path.join(resource_path, 'Interfaces') # The image folder path
rel_path="Interfaces/"
abs_file_path=os.path.join(current_path,rel_path)
current_file="add.png"
#load= Image.open(abs_file_path+current_file)
#photo=ImageTk.PhotoImage(load)
Path_F=tk.Entry(root,state=tk.DISABLED,width=27, bd=6, textvariable=v )
Path_F.pack(ipady=50)
Path_F.place(x=150, y=200, in_=root)

photo=PhotoImage(file=abs_file_path+current_file)
#photo_bu=photo.
photo_bu=photo.subsample(18,18)
openFile=tk.Button(root, image=photo_bu, bg="white", command=getfile, relief=RAISED)
#openFile.pack()
openFile.place(x=390, y=197, in_=root)

Search_F=tk.Button(root, text="Buscar", relief=FLAT)
Search_F.place(x=240, y=260, in_=root)

current_help="ayuda.png"
help_=PhotoImage(file=abs_file_path+current_help)
help_ima=help_.subsample(30,28)
h_button=tk.Button(root,image=help_ima,text="Ayuda",font=("Arial Black",20), bg="white", relief=FLAT, compound="left" )
h_button.place(x=50,y=400, in_=root)
root.mainloop()