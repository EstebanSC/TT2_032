import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 
from LectCI import *
import threading
import os 
import time
### Definicion de la pantalla descargas, implementar GIF'S
class WaitSearchData():
    compounds=[] #Arreglos globales de compuestos
    proteins=[]#Arreglos proteinasn
    project_path=""#Directorio del proyecto
    def __init__(self):
        current_path = os.path.dirname(__file__) # Where your .py file is located
        self.pantalla=tk.Toplevel()
        self.pantalla.resizable(False, False)
        self.pantalla.protocol("WM_DELETE_WINDOW", self.ask_quit)
        self.telacontrol=Canvas(self.pantalla,height=450,width=850,bg="white" )
        self.telacontrol.pack(expand=FALSE)
        self.title=tk.StringVar()
        self.r="Iniciando Busqueda de Datos"
        self.title.set(self.r)
        self.header=Label(self.pantalla,textvariable=self.title,bg="white")
        self.header.configure(font=("Arial Black",26))
        self.header.config(justify=CENTER)
        self.header.pack()
        #rel_path="Interfaces/"
        #abs_file_path=os.path.join(current_path,rel_path)
        #current_file="giphy.gif"
        #self.photo=PhotoImage(file=abs_file_path+current_file, format="gif -index 2")
        #self.photo_bu=self.photo.subsample(1,1)
        #self.charge=Label(self.pantalla,height=400, width=400, image=self.photo_bu,bg="white")
        self.charge=Progressbar(self.pantalla,mode="indeterminate",maximum=25)
        #self.charge.step(2)
        #self.hilo=threading.Thread(target=connect_DrugBank(compounds, project_path))
        #self.hilo.start()
        #self.ver()
    
    def ver(self):
        #global compounds
        #global proteins
        self.pantalla.title("Buscando Datos...")
        self.pantalla.geometry("850x450")
        self.center_screen()
        self.header.place(x=25,y=50)
        self.charge.place(x=250,y=250, width=350)
        self.charge.start()
        ######Esta parte sigue en proceso
        #data_presc=threading.Thread(target=connect_DrugBank, args=(proteins,project_path))
        #data_presc.start()
        ########        
       
    def ask_quit(self):
        if messagebox.askokcancel("Cerrar", "Desea cerrar la busqueda de datos ?"):
            self.pantalla.destroy()
    
    def center_screen(self):
       self.pantalla.update_idletasks()
       w = self.pantalla.winfo_screenwidth()
       h = self.pantalla.winfo_screenheight()
       size = tuple(int(_) for _ in self.pantalla.geometry().split('+')[0].split('x'))
       x = w/2 - size[0]/2
       y = h/2 - size[1]/2
       self.pantalla.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def  procesos(self,compounds,proteins,project_path):
        #time.sleep(10)
        show_s=threading.Thread(target=self.ver)
        #ct0=threading.Thread(target=self.change_title)
        get_compounds=threading.Thread(target=alldata_compunds,args=(compounds,project_path))
       # ct1=threading.Thread(target=self.change_title)
        get_proteins=threading.Thread(target=connect_PDB, args=(proteins,project_path))
        show_s.start()
        self.r="Comenzando Busqueda de Datos de Compuestos "
        #ct0.start()
        get_compounds.start()
        self.r="Comenzando Busqueda de Datos de Proteinas "
        #ct1.start()
        get_proteins.start()
    
    def change_title(self):
        #self.r=te
        time.sleep(5)
        self.title.set(self.r)
        self.header.configure(textvariable=self.title)
        