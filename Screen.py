import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 

import os 

def search_r(compounds):

    top = tk.Toplevel()
    top.title("Buscando Datos..")
    top.wm_attributes('-alpha',0.1)
    top.resizable(False,False)
    top.geometry("800x450")
    
    canvas=tk.Frame(top,height=450,width=800,bg="white" )
    canvas.pack(expand=False)
    #############################
    textf=tk.Label(top, bg="white",text="Buscando Datos de Compuestos...")
    textf.configure(font=("Arial Black",26))
    textf.place(x=100,y=50, in_=top)
    ##############################
    current_path = os.path.dirname(__file__) # Where your .py file is located
    rel_path2="Interfaces/"
    abs_file_path2=os.path.join(current_path,rel_path2)
    #current_log="correcto.png"
    current_log="Waiting.gif"
    photo_log= PhotoImage(file=abs_file_path2+current_log)
    #photo_log.configure(heigth=20, width=30)
    pp=photo_log.subsample(1,1)
    gif_wait=tk.Label(top,height=250, width=250, image=pp,bg="white")
    gif_wait.place(x=300,y=200,in_=top)
    

    top.mainloop()
    


