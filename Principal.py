import tkinter as tk
from tkinter.ttk import *
from tkinter import  filedialog, Text , messagebox
from PIL import Image, ImageTk  
from LectCI import *
import SearchInfoScreen
from First_S import *
from pathlib import Path
import os
import errno
import threading
import CheckConnection
from CustomSpanishDialog import *
import queue as queue
import time

exCompounds= []
exProteins = []
isConnected = True
drugclass = ''

##Se Inicia la pantalla es el archivo que carga la pantalla
class Principal():

    def __init__(self):
        self.threadCounter = 0
        self.lock = threading.Lock()
        self.queue = queue.Queue()
        #GUI
        self.pantalla=tk.Tk()
        self.pantalla.resizable(False, False)
        self.pantalla.protocol("WM_DELETE_WINDOW", self.ask_quit)
        current_path = os.path.dirname(__file__) # Where your .py file is located
        self.FrameP=Canvas(self.pantalla,height=400,width=550,bg="white")
        self.FrameP.pack(expand=FALSE)
        self.Titulo1=Label(self.pantalla,text="Sistema para la Predicción",bg="white")
        self.Titulo1.config(font=("Arial",16))
        self.Titulo2=Label(self.pantalla,text="de Actividad Farmacológica",bg="white")
        self.Titulo2.config(font=("Arial",16))
        rel_path2="Logotipo/"
        abs_file_path2=os.path.join(current_path,rel_path2)
        current_log="Logotipo.png"
        self.photo_log=PhotoImage(file=abs_file_path2+current_log)
        self.pp=self.photo_log.subsample(18,18)
        self.LogoP=Label(self.pantalla,height=150, width=150, image=self.pp,bg="white")
        self.createProject=Button(self.pantalla,text="Nuevo Proyecto",relief=FLAT,width=14,height=2,command=self.newProject)
        self.existingProject=Button(self.pantalla,text="Abrir Proyecto",relief=FLAT,width=14,height=2,command=self.exProject)
        self.ver()

    def ver(self):
        self.pantalla.title("SisPAF")
        self.pantalla.geometry("550x400")
        self.center_screen()
        self.Titulo1.place(x=250, y=70)
        self.Titulo2.place(x=245, y=100)
        self.LogoP.place(x=30,y=30)
        self.createProject.place(relx=0.5,rely=0.6,anchor=CENTER)
        self.existingProject.place(relx=0.5,rely=0.8,anchor=CENTER)
        #AQUI HAY QUE POSICIONAR LOS COMPONENTES
        self.pantalla.mainloop()

    def center_screen(self):
       self.pantalla.update_idletasks()
       width = self.pantalla.winfo_width()
       height = self.pantalla.winfo_height()
       x = (self.pantalla.winfo_screenwidth() // 2) - (width // 2)
       y = (self.pantalla.winfo_screenheight() // 2) - (height // 2)
       self.pantalla.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def ask_quit(self):
        if messagebox.askokcancel("CERRAR", "¿Desea cerrar SisPAF?"):
            self.pantalla.destroy()
    
    def newProject(self):
        self.newPath = self.create_path()
        cPath = self.newPath + '/Compounds'
        pPath = self.newPath + '/Proteins'
        dPath = self.newPath + '/DockingLib'
        fPath = self.newPath + '/CI_copy.txt'

        if(os.path.isdir(cPath) and os.path.isdir(pPath) and os.path.isfile(fPath)):
            #print('Si estan los directorios')
            #msgbox = CustomSpanishDialog()
            #resultmsg = msgbox.getValue()
            #print(resultmsg)
            msgbox = messagebox.askyesno('ALERTA','En este directorio ya existe un proyecto. Crear uno nuevo sobreescribirá el proyecto existente. ¿Desea continuar?',parent=self.pantalla)
            if msgbox:      #Sobreescribimos proyecto
                try:
                    self.overwriteProject(cPath)    #Eliminamos todo lo que hay en el directorio de compuestos
                    self.overwriteProject(pPath)    #Eliminamos todo lo que hay en el directorio de proteinas
                    self.overwriteProject(dPath)    #Eliminamos todo lo que hay en el directorio de docking
                    os.remove(fPath)                #Eliminamos copia de conjunto inicial
                except:
                    pass
                #self.pantalla.destroy()
                self.createProject["state"] = "disabled"
                self.existingProject["state"] = "disabled"
                First=First_S(self.newPath,self.createProject,self.existingProject)
        else:
            #self.pantalla.destroy()     #ESTO DEBE CAMBIARSE POR UN BOTON DE BACK
            self.createProject["state"] = "disabled"
            self.existingProject["state"] = "disabled"
            First=First_S(self.newPath, self.createProject, self.existingProject)
    
    def overwriteProject(self,overwritepath):
        fileList = [ f for f in os.listdir(overwritepath)]
        for f in fileList:
            os.remove(os.path.join(overwritepath,f))
        

    def exProject(self):
        global drugclass
        self.exPath = self.create_path()
        self.initCompounds = []
        self.initProteins = []

        if(os.path.isfile(self.exPath + '/CI_copy.txt')):
            [self.initCompounds,self.initProteins] = lectura(self.exPath + '/CI_copy.txt')
            drugclass = getDrugClass()
            if(self.initCompounds==[] or self.initProteins==[]):
                messagebox.showerror(title="ERROR", message="!El archivo no contiene los datos necesarios!")
            else:
                self.lenCompounds = len(self.initCompounds)
                self.lenProteins = len(self.initProteins)
        self.lookingForProject()

    def create_path(self):
        self.project_path = ''
        home = str(Path.home())
        self.project_path=filedialog.askdirectory(initialdir=home, title="Seleccione el directorio del proyecto")
        #print(project_path)
        return self.project_path
    
      #####################################################################}
    def NoRepeat(self,Noclean,Clean):
        for x in Noclean:
            if x not in Clean:
                Clean.append(x)
        return Clean


    def lookingForProject(self):
        global exCompounds
        global exProteins
        compoundsPath = self.exPath + '/Compounds'
        proteinsPath = self.exPath + '/Proteins'
        copyInitFilePath = self.exPath + '/CI_copy.txt'
        compoundThreads = list()
        proteinThreads = list()
        #Inicializamos los arreglos que vamos a modificar, realizando una copia del resultado de leer el
        #archivo inicial
        if not (self.initCompounds==[] and self.initProteins==[]):
            self.master = tk.Toplevel()
            exCompounds = self.initCompounds.copy()
            exProteins = self.initProteins.copy()
        #Revisar que exista un folder de compuestos y proteinas, si no es así, regresar a la pantalla
        #principal y notificar al usuario
        if(os.path.isdir(compoundsPath) and os.path.isdir(proteinsPath) and os.path.isfile(copyInitFilePath)):
            #Si los dos directorios estan vacios, sera como un nuevo proyecto
            if (len(os.listdir(compoundsPath)) == 0 and len(os.listdir(proteinsPath))):
                self.pantalla.destroy()
                First=First_S(self.newPath)
            else:       #Analizamos proyecto
                #AQUI VA LA INTERFAZ
                C_noclean=self.initCompounds
                P_noclean=self.initProteins
                self.initProteins=[]
                self.lenCompounds=[]
                self.initCompounds=self.NoRepeat(C_noclean,self.initCompounds)
                self.initProteins=self.NoRepeat(P_noclean,self.initProteins)

                self.loadingScreen = LoadingProjectScreen(self.master,self.queue, self.lenCompounds, self.lenProteins,self.exPath,self.createProject,self.existingProject)
                self.loadingScreen.showScreen()
                self.createProject["state"] = "disabled"
                self.existingProject["state"] = "disabled"
                #self.pantalla.destroy()

                for item in self.initCompounds:   #Analizamos cada elemento del arreglo de compuestos
                    getCompound = threading.Thread(target=self.checkProject,args=(item,'compounds'))
                    compoundThreads.append(getCompound)
                    getCompound.start()
                
                for item in self.initProteins:
                    getProtein = threading.Thread(target=self.checkProject,args=(item,'proteins'))
                    proteinThreads.append(getProtein)
                    getProtein.start()
                
                self.periodic_call()
                
            #self.checkProject() #Aqui se comienza a analizar el projecto (ESTO DEBE DE SER CON HILOS)
        else:
            messagebox.showerror('ERROR', 'No se encontro ningún proyecto')
    
    def checkProject(self,data,case):
        global exCompounds
        global exProteins
        verifiedPath = ''
        #Para ajustar a los directorios de compuestos o proteinas
        if case == 'compounds':
            verifiedPath = self.exPath + '/Compounds'
            line = 'c0' + data + '.pdb'
            print('ya configure el archivo: ' + line)
        elif case == 'proteins':
            verifiedPath = self.exPath + '/Proteins'
            line = 'cP' + data + '.pdb'
        
        #Analizamos cada archivo del directorio
        
        for root, dirs, files in os.walk(verifiedPath):
                for file in files:
                    if line == file:        #Si el nombre del archivo coincide con el del elemento en el array
                        if case == 'compounds':     #Estamos en compounds
                            #print('Debo eliminar: ' + data)
                            exCompounds.remove(data)   #Eliminamos el elemento del array porque ya existe
                        elif case == 'proteins':                   #Estamos en proteinas
                            #print('Debo eliminar: ' + data)
                            exProteins.remove(data)
                    
        #Leer cada archivo y revisar si esta completa la info

        try:
            with open(os.path.join(verifiedPath,line), 'rb') as f:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
                last_line = f.readline().decode()

                if case == 'compounds':
                    if last_line.strip() != 'FINAL':
                        #print('Debo agregar: ' + data)
                        exCompounds.append(data)
                elif case == 'proteins':
                    if last_line.strip() != 'END':
                        #print('Debo agregar: ' + data)
                        exProteins.append(data)
        except:
            pass
        
        #Ya terminamos, revisamos si el proyecto ya esta completo y notificamos a la pantalla
        if len(exCompounds) == 0 and len(exProteins) == 0:
            #El proyecto ya termino la busqueda de informacion. De aqui pasamos directamente al analisis
            print('Proyecto directo al analisis')

        #print('Ya acabe con: ' + str(data))
        self.lock.acquire()      #Cada hilo bloquea el recurso g porque es un valor critico
        self.threadCounter += 1         #Se aumenta el valor
        self.lock.release()      #Se libera el recurso
        msg = self.threadCounter        #El valor de g se asigna al mensaje que se pondrá en la cola de mensajes
        self.queue.put(msg) #Se envia el mensaje a la cola de mensajes
        return


    def periodic_call(self):        #Funcion para checar la cola de mensajes
        self.master.after(200, self.periodic_call)  #Cada 200 ms se llama a si misma y llama a incomingProcess
        self.loadingScreen.incomingProcess()      #Aqui se procesa lo que hay en la cola de mensajes

class LoadingProjectScreen():

    def __init__(self,master,queue,lenCompouds,lenProteins,path,buttonReferenced1,buttonReferenced2):
        self.queue = queue
        self.pantalla = master
        self.lengthCompounds = lenCompouds
        self.lengthProteins = lenProteins
        self.buttonRef1 = buttonReferenced1
        self.buttonRef2 = buttonReferenced2
        self.project_path = path
        self.pantalla.resizable(False, False)
        self.pantalla.protocol("WM_DELETE_WINDOW", self.ask_quit)
        self.telacontrol=Canvas(self.pantalla,height=200,width=400,bg="white")
        self.telacontrol.pack(expand=FALSE)
        self.title=tk.StringVar()
        self.r="Cargando proyecto..."
        self.title.set(self.r)
        self.header=Label(self.pantalla,textvariable=self.title,bg="white")
        self.header.configure(font=("Arial Black",20))
        #self.header.config(anchor=CENTER)
        self.header.pack()
        self.charge=Progressbar(self.pantalla,mode="indeterminate",maximum=25)
    
    def showScreen(self):       #Funcion para mostrar la pantalla
        self.pantalla.title("Carga de proyecto")
        self.pantalla.geometry("400x200")
        CenterScreen.center_screen(self.pantalla)
        self.header.place(relx=0.5,rely=0.2,anchor=CENTER)
        self.charge.place(relx=0.5,rely=0.7, width=200,anchor=CENTER)
        self.charge.start()
        #time.sleep(3)
       
    def ask_quit(self):         #Funcion para el cuadro de dialogo que permita cerrar la ventana
        if messagebox.askokcancel("CERRAR", "¿Desea cerrar la carga del proyecto?",parent=self.pantalla):
            self.pantalla.destroy()
            self.buttonRef1["state"] = ["normal"]
            self.buttonRef2["state"] = ["normal"]
    
    def incolmingProcess(self):      #Funcion que permite a la ventana "atender" lo que hacen los hilos
                                    #Asi evitamos que la interfaz se "congele" mientras los hilos trabajan
        while self.queue.qsize():
            try:
                msg = self.queue.get_nowait()       #Existe una cola de mensajes donde los hilos escriben
                #print(msg)
                if msg == (self.lengthCompounds + self.lengthProteins):    #Si el mensaje es igual al tamaño 
                                                                             #de la suma de los arreglos significa
                                                                             #que los hilos ya terminaron           
                    #print('Ya acabe de analizar el proyecto')
                    print(exCompounds)
                    print(exProteins)
                    self.beginSearch()
                    #self.show_results()
            except queue.Empty:
                pass
        
    def beginSearch(self):
        global exCompounds
        global exProteins
        global isConnected
        global drugclass

        isConnected = CheckConnection.check_internet_conn()
        if isConnected:     #Si el usuario esta conectado, comenzar busqueda de datos
            #Instanciando la clase de los hilos (ThreadClient)
            tc = SearchInfoScreen.ThreadedClient(drugclass,exCompounds,exProteins,self.project_path,self.buttonRef1, self.buttonRef2)
            self.pantalla.destroy()
        else:   #Si no lo esta, mostrar message box donde indique al usuario que debe estar conectado a internet
            self.ask_check()
    
    def ask_check(self):    #Cuando el usuario da click en OK, se vuelve a revisar que se tenga internet
        if messagebox.showerror("ERROR", "Asegurese que se encuentra conectado a internet",parent=self.pantalla):
            isConnected = CheckConnection.check_internet_conn()

Principal = Principal()
#First.ver()