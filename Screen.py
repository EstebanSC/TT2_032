import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 
from LectCI import *
import threading
import os 

### Definicion de la pantalla descargas, implementar GIF'S
class WaitSearchData():
    compounds=[] #Arreglos globales de compuestos
    proteins=[]#Arreglos proteinas
    project_path=""#Directorio del proyecto
    def __init__(self):
        self.pantalla=tk.Tk()
        self.pantalla.protocol("WM_DELETE_WINDOW", self.ask_quit)
        self.telacontrol=Canvas(self.pantalla,height=450,width=850,bg="white" )
        self.telacontrol.pack(expand=FALSE)
        self.header=Label(self.pantalla, bg="white",text="Buscando Datos de Compuestos...")
        self.header.configure(font=("Arial Black",26))
        #self.hilo=threading.Thread(target=connect_DrugBank(compounds, project_path))
        #self.hilo.start()
        #self.ver()
    
    def ver(self, compounds,proteins, project_path):
        #global compounds
        #global proteins
        self.pantalla.title("Buscando Datos...")
        self.pantalla.geometry("850x450")
        self.header.place(x=100,y=50)
        print(compounds)
        print(proteins)
        print(project_path)
        #self.pantalla.after(0, )
        data_esc=threading.Thread(target=connect_DrugBank, args=(compounds,project_path))
        #ver_p=threading.Thread(target=self.pantalla.mainloop())
        data_esc.start()
        ######Esta parte sigue en proceso
         #data_presc=threading.Thread(target=connect_DrugBank, args=(proteins,project_path))
        #data_presc.start()
        ########        
        #ver_p.start()
        #self.pantalla.mainloop()
    def ask_quit(self):
        if messagebox.askokcancel("Cerrar", "Desea cerrar la busqueda de datos ?"):
            self.pantalla.destroy()
