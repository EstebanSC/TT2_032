import tkinter as tk
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 

import os 
root = tk.Tk()
root.geometry("900x500")


current_path = os.path.dirname(__file__) # Where your .py file is located
f1 = tk.Frame(root, background="white", height=600,width=1100)
#f2 = tk.Frame(root, background="pink")
f1.pack(expand=False)

rel_path2="Logotipo/"
abs_file_path2=os.path.join(current_path,rel_path2)
current_log="SisPAF.png"
Iso=PhotoImage(file=abs_file_path2+current_log)
Iso_lo=Iso.subsample(15,15)
logo_f=tk.Label(root, image=Iso_lo, height=100, width=400, bg="white")
logo_f.place(x=500, y=10, in_=root)
button = tk.Button(root, text="Iniciar", bg="green")
button.place(x=700, y=400, in_=root)


rel_path="Interfaces/"
abs_file_path=os.path.join(current_path,rel_path)
current_help="ayuda.png"
help_=PhotoImage(file=abs_file_path+current_help)
help_ima=help_.subsample(30,30)
h_button=tk.Button(root,image=help_ima,text="Ayuda",font=("Arial Black",20), bg="white", relief=FLAT, compound="left" )
h_button.place(x=50,y=400, in_=root)


rel_path_plus="Interfaces/Pantallas/"
abs_file_path_3=os.path.join(current_path,rel_path_plus)
current_p="Tutorial2.png"
prin_I=PhotoImage(file=abs_file_path_3+current_p)
PI_P=prin_I.subsample(2,2)

foto_Lab=tk.Label(root,image=PI_P)
foto_Lab.place(x=10, y=10, in_=root)
root.mainloop()