import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text , messagebox
from PIL import Image, ImageTk 
from Threads_CS import *
from LectCI import *
from Screen import *
from pathlib import Path
import os
import errno

compounds=[] #Arreglos globales de compuestos
proteins=[]#Arreglos proteinas
project_path=""#Directorio del proyecto


class First_S():
    def __init__(self):
        
        self.pantalla=tk.Tk()
        self.pantalla.resizable(False, False)
        self.pantalla.protocol("WM_DELETE_WINDOW", self.ask_quit)
        current_path = os.path.dirname(__file__) # Where your .py file is located
        self.v=tk.StringVar()
        self.create_path()
        try:
            #os.makedirs(current_path+"/Proteins/")#Creacion de Directorio para proteinas
            #os.makedirs(current_path+"/Compounds/")#Creacion de Directorio Compounds
            os.makedirs(project_path+"/Proteins/")#Creacion de Directorio para proteinas
            os.makedirs(project_path+"/Compounds/")#Creacion de Directorio Compounds
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        self.FrameP=Canvas(self.pantalla,height=600,width=1100,bg="white")
        self.FrameP.pack(expand=FALSE)
        self.TituloP=Label(self.pantalla,text="Sistema para la Prediccion de Actividad Farmacologica",bg="White")
        self.TituloP.config(font=("Arial",26))
        rel_path2="Logotipo/"
        abs_file_path2=os.path.join(current_path,rel_path2)
        current_log="Logotipo.png"
        self.photo_log=PhotoImage(file=abs_file_path2+current_log)
        self.pp=self.photo_log.subsample(5,5)
        self.LogoP=Label(self.pantalla,height=400, width=400, image=self.pp,bg="white")
        self.Buscar_A=Label(self.pantalla,text="Buscar Archivo",bg="White")
        self.Buscar_A.config(font=("Arial",18))
        rel_path="Interfaces/"
        abs_file_path=os.path.join(current_path,rel_path)
        current_file="add.png"
        self.Path_F=Entry(self.pantalla,state=tk.DISABLED,width=25, bd=2, textvariable=self.v ,font=("Arial",12))
        self.Path_F.pack(ipady=50)
        self.photo=PhotoImage(file=abs_file_path+current_file)
        self.photo_bu=self.photo.subsample(18,18)
        self.openFile=Button(self.pantalla,image=self.photo_bu, bg="white", command=self.getfile, relief=RAISED)
        self.Search_F=Button(self.pantalla,text="Iniciar", relief=FLAT, state=DISABLED,command=self.begin_all)
        current_help="ayuda.png"
        self.help_=PhotoImage(file=abs_file_path+current_help)
        self.help_ima=self.help_.subsample(30,28)
        self.hbutton=Button(self.pantalla,image=self.help_ima,text="Ayuda",font=("Arial Black",20), bg="white", relief=FLAT, compound="left" )
        self.ver()
    
    #######Las funciones se declaran aqui ##################
    #####Funcion de Ruta proyecto##########
    def ver(self):
        self.pantalla.title("SISPAF")
        self.pantalla.geometry("900x500")
        self.TituloP.place(x=30, y=30)
        self.LogoP.place(x=480, y=90)
        self.Buscar_A.place(x=180,y=150)
        self.Path_F.place(x=150,y=200)
        self.openFile.place(x=390,y=197)
        self.Search_F.place(x=240,y=260)
        self.hbutton.place(x=50,y=400)
        self.pantalla.mainloop()
    def ask_quit(self):
        if messagebox.askokcancel("Cerrar", "Desea cerrar SISPAF ?"):
            self.pantalla.destroy()
    def create_path(self):
        global project_path
        home = str(Path.home())
        project_path=filedialog.askdirectory(initialdir=home, title="Seleccione el directorio del Proyecto")
        print(project_path)
#####Funcion de Lectura de Archivo############
    def getfile(self):
        global compounds
        global proteins
        home = str(Path.home())
        filename=filedialog.askopenfilename(initialdir=home,title="Seleccione Archivo",
        filetypes=(("text","*.txt"),("all files","*.txt")))
        #txtf=Path_F.get()
        txtf=str(filename)##Para convertir a String y se separa por /
        print(txtf)#
        Arr=txtf.split('/')
        r=Arr.pop()#Se obtiene el ultimo elemento del arreglo, que es el nombre del archivo
        print(r)
    #print(Arr[4])
        self.v.set(r)
        [compounds,proteins]=lectura(filename)
        if(compounds==[] or proteins==[]):
            messagebox.showerror(title="ERROR", message="El Archivo no contiene los datos necesarios!")
        else:
            self.Search_F.configure(state=NORMAL, bg="green")
        
    #####################################################################
    #################Esta funcion es la que inicia despues de validar el documento#################
    #########################Funcion llamada por el boton con texto aleatorio######################
    def begin_all(self):
        global compounds
        global proteins
        get_data(compounds,proteins,project_path)
        #search_r()

