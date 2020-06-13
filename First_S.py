import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text , messagebox
from PIL import Image, ImageTk 
from Threads_CS import *
from LectCI import *
import SearchInfoScreen
import CheckConnection
from pathlib import Path
import os
import errno
import urllib
import shutil
import CenterScreen

compounds=[] #Arreglos globales de compuestos
proteins=[]#Arreglos proteinas
project_path=""#Directorio del proyecto


class First_S():
    def __init__(self,path,refButton1,refButton2):

        self.pantalla=tk.Toplevel()
        self.refButton1 = refButton1
        self.refButton2 = refButton2
        self.buttonSet = False
        self.refButton1["state"] = ["disabled"]
        self.refButton2["state"] = ["disabled"]
        self.pantalla.resizable(False, False)
        self.pantalla.protocol("WM_DELETE_WINDOW", self.ask_quit)
        current_path = os.path.dirname(__file__) # Where your .py file is located
        self.project_path = path
        #print(self.project_path)
        self.v=tk.StringVar()
        try:
            #os.makedirs(current_path+"/Proteins/")#Creacion de Directorio para proteinas
            #os.makedirs(current_path+"/Compounds/")#Creacion de Directorio Compounds
            os.makedirs(self.project_path+"/Proteins/")#Creacion de Directorio para proteinas
            os.makedirs(self.project_path+"/Compounds/")#Creacion de Directorio Compounds
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
        self.Search_F=Button(self.pantalla,text="Iniciar", relief=FLAT,state=DISABLED,command=self.begin_all)
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
        CenterScreen.center_screen(self.pantalla)
        self.TituloP.place(x=30, y=30)
        self.LogoP.place(x=480, y=90)
        self.Buscar_A.place(x=180,y=150)
        self.Path_F.place(x=150,y=200)
        self.openFile.place(x=390,y=197)
        self.Search_F.place(x=240,y=260)
        self.hbutton.place(x=50,y=400)
        self.pantalla.mainloop()

    def ask_quit(self):
        if messagebox.askokcancel("Cerrar", "Desea cerrar SISPAF ?", parent=self.pantalla):
            self.refButton1["state"] = ["normal"]
            self.refButton2["state"] = ["normal"]
            self.pantalla.destroy()

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
        #Hacer la copia en el directorio
        shutil.copyfile(txtf,(self.project_path + '/CI_copy.txt'))
        Arr=txtf.split('/')
        r=Arr.pop()#Se obtiene el ultimo elemento del arreglo, que es el nombre del archivo
        print(r)
    #print(Arr[4])
        self.v.set(r)
        [compounds,proteins]=lectura(filename)
        if(compounds==[] or proteins==[]):
            messagebox.showerror(title="ERROR", message="El Archivo no contiene los datos necesarios!")
        else:
            C_noclean=compounds
            P_noclean=proteins
            compounds=[]
            proteins=[]
            compounds=self.NoRepeat(C_noclean,compounds)
            proteins=self.NoRepeat(P_noclean,proteins)
            self.Search_F.configure(state=NORMAL, bg="green")
        
    #####################################################################}
    def NoRepeat(self,Noclean,Clean):
        for x in Noclean:
            if x not in Clean:
                Clean.append(x)
        return Clean
    ################################
    #################Esta funcion es la que inicia despues de validar el documento#################
    #########################Funcion llamada por el boton con texto aleatorio######################
    def begin_all(self):
        global compounds
        global proteins
        #Revisar que el usuario este conectado a internet
        isConnected = CheckConnection.check_internet_conn()
        if isConnected:     #Si el usuario esta conectado, comenzar busqueda de datos
            #Deshabilitamos botones
            self.Search_F["state"] = ["disabled"]
            self.openFile["state"] = ["disabled"]
            #Instanciando la clase de los hilos (ThreadClient)
            if not self.buttonSet:
                tc = SearchInfoScreen.ThreadedClient(compounds,proteins,self.project_path,self.openFile,self.Search_F)
                self.buttonSet = True
            else:
                msgbox = messagebox.askyesno('Alerta','En este directorio ya existe un proyecto. Comenzar uno nuevo sobreescribirá el proyecto existente. ¿Desea continuar?',parent=self.pantalla)
                if msgbox:      #Sobreescribimos proyecto
                    try:
                        self.overwriteProject(self.project_path + 'Compounds')    #Eliminamos todo lo que hay en el directorio de compuestos
                        self.overwriteProject(self.project_path + '/Proteins')    #Eliminamos todo lo que hay en el directorio de proteinas
                        os.remove(self.project_path + '/CI_copy.txt')                #Eliminamos copia de conjunto inicial
                    except:
                        pass
                    tc = SearchInfoScreen.ThreadedClient(compounds,proteins,self.project_path,self.openFile,self.Search_F)    
        else:   #Si no lo esta, mostrar message box donde indique al usuario que debe estar conectado a internet
            self.ask_check()
        #search_r()
        #tc = SearchInfoScreen.ThreadedClient(compounds,proteins,project_path)
        
    def overwriteProject(self,path):
        fileList = [ f for f in os.listdir(path)]
        for f in fileList:
            os.remove(os.path.join(path,f))

    def ask_check(self):    #Cuando el usuario da click en OK, se vuelve a revisar que se tenga internet
        if messagebox.showerror("Revisar conexion", "Asegurese que se encuentra conectado a internet",parent=self.pantalla):
            isConnected = CheckConnection.check_internet_conn()

