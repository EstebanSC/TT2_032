import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 
from LectCI import *
import threading
import os 

### Definicion de la pantalla descargas, implementar GIF'S
def search_r():

    top = tk.Toplevel()
    top.title("Buscando Datos..")
    top.wm_attributes('-alpha',0.1)
    top.resizable(False,False)
    top.geometry("800x450")
    
    canvas=tk.Frame(top,height=450,width=800,bg="white" )
    canvas.pack(expand=False)
    #############################
    current_path = os.path.dirname(__file__) # Where your .py file is located
    rel_path2="Interfaces/"
    abs_file_path2=os.path.join(current_path,rel_path2)
    #current_log="correcto.png"
    current_log="Waiting.gif"
    photo_log= PhotoImage(file=abs_file_path2+current_log)
    pp=photo_log.subsample(1,1)
    textf=tk.Label(top, bg="white",text="Buscando Datos de Compuestos...")
    textf.configure(font=("Arial Black",26))
    gif_wait=tk.Label(top,text="Check",bg="white", image=pp)
    gif_wait.configure(font=("Arial Black",26), height=250, width=250)
    gif_wait.place(x=300,y=200,in_=top)
    textf.place(x=100,y=50, in_=top)
    ##############################
    
    #gif_wait=tk.Label(top,height=250, width=250, text="Check",bg="white")
    #gif_wait.place(x=300,y=200,in_=top)
    #gif_wait.pack()
    #top.update_idletasks()
    #top.update()f
    top.wm_transient(master=None)  #Con True si  Wtse ve la imagenWTf
    #Funcion para obtener el id del compuesto de acuerdo a DrugBank
    



