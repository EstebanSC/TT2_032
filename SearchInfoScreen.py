#Imports generales
import os
import time
import urllib
import CheckConnection
#Imports para la interfaz
import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from tkinter import  filedialog, Text, messagebox
from PIL import Image, ImageTk 
from LectCI import *
from pruebapdb import *
from getids import *
from Bio.PDB import PDBList
import CenterScreen
#Imports para los hilos
import threading
import queue as queue
#Imports para PubChem
import pubchempy as pcp
import json
#Imports para web scraping
from selenium import webdriver
from Bio.PDB import *
from selenium.webdriver.common.keys import Keys
import requests
from pypdb import find_results_gen
import time
from ratelimit import limits, sleep_and_retry
import multiprocessing as mp
import pandas as pd
import operator
from sklearn.linear_model import LinearRegression
import pickle



#Definicion de la pantalla descargas
isConnected = True                  #Esta es una condicion que se estara checando cuando se hagan
                                    #las llamadas a las API o se use internet. Es True puesto que
                                    #First_S.py ya se checo el internet y si esta aqui es por que si hay
event = threading.Event()
#COmpuestos o proteinas no encontrados
Compounds=[]
Proteins=[]
compoundsMDB1=[]#Compuestos Perdidos DB1
compoundsMDB2=[]#Compuesto Perdidos DB2
P_notfounds=[] #Proteinas Perdidas
compoundsMissed=[] #Compuestos Pub
RealCompounds=[]
RealProteins=[]
dc = '' #clase de los medicamentos
class GUISection:

    def __init__(self, master, queue, project_path, lenCompounds, lenProteins,refButton1,refButton2):      #Constructor de la clase
        current_path = os.path.dirname(__file__) # Where your .py file is located
        self.queue = queue
        self.pantalla = master
        self.length_compounds = lenCompounds
        self.length_proteins = lenProteins
        self.project_path = project_path
        self.refButton1 = refButton1
        self.refButton2 = refButton2
        self.pantalla.resizable(False, False)
        self.pantalla.protocol("WM_DELETE_WINDOW", self.ask_quit)
        self.telacontrol=Canvas(self.pantalla,height=450,width=950,bg="white" )
        self.telacontrol.pack(expand=FALSE)
        self.title=tk.StringVar()
        self.r="Buscando datos..."
        self.title.set(self.r)
        self.header=Label(self.pantalla,textvariable=self.title,bg="white", anchor="n")
        self.header.configure(font=("Arial Black",26))
        #self.header.config(anchor=CENTER)
        self.header.pack()
        self.charge=Progressbar(self.pantalla,mode="indeterminate",maximum=25)
        self.charge.pack()    

    def showScreen(self):       #Funcion para mostrar la pantalla
        self.pantalla.title("Búsqueda")
        self.pantalla.geometry("950x450")
        #self.pantalla.title("Búsqueda")
        #self.pantalla.geometry("850x450")
        CenterScreen.center_screen(self.pantalla)
        self.header.place(x=325,y=25)
        self.charge.place(x=275,y=225, width=450)
        self.charge.start()
        #time.sleep(3)
       

    def ask_quit(self):         #Funcion para el cuadro de dialogo que permita cerrar la ventana
        if messagebox.askokcancel("Cerrar", "¿ Desea cerrar la tarea en proceso ?",parent=self.pantalla):
        #if messagebox.askokcancel("Cerrar", "¿Desea cerrar la búsqueda de datos?",parent=self.pantalla):
            self.refButton1["state"] = ["normal"]
            self.refButton2["state"] = ["normal"]
            self.pantalla.destroy()

    #NOTA: ESTO ES UNA FUNCION PARA PRUEBAS VISUALES
    def search_end(self):
        #self.change_title("Finalizando busqueda...",2)
        #self.change_title("Recopilando resultados...",3)
        self.header.place(x=200,y=25)
        self.change_title("RESULTADOS DE LA BÚSQUEDA")
        self.charge.destroy()
        #self.telacontrol.destroy()
        self.charge_results()
    
    def ini_analisis(self):
        self.container.destroy()
        self.containerP.destroy()
        self.B_Analisis.destroy()
        self.B_Salir.destroy()
        self.pantalla.title('Análisis')
        self.header.place(x=300,y=25)
        self.change_title("Analizando los datos...")
        self.charge=Progressbar(self.pantalla,mode="indeterminate",maximum=25)
        self.charge.place(x=275,y=225, width=450)
        self.charge.start()

       
       # self.change_title("RESULTADOS DE LA BÚSQUEDA")
        #self.charge.pack_forget()   #Esconde la barra de progreso pero no la elimina (ESTO NO FUNCIONA)

        #Crear boton de continuar, si se hace clic en el nos lleva a una nueva clase (ANALISIS)
        #NOTA PARA STEVE: EL BOTON SI FUNCIONA, PERO LA BARRA DE PROGRESO NO PUEDO OCULTARLA
        #elf.continueProject=Button(self.pantalla,text="Continuar",relief=FLAT,width=14,height=2,command=self.analizeProject)
        #elf.continueProject.place(relx=0.5,rely=0.8,anchor=CENTER)

    def analizeProject(self):
        self.container.destroy()
        self.containerP.destroy()
        self.B_Analisis.destroy()
        self.B_Salir.destroy()
        self.header.place(x=300,y=25)
        self.change_title("Analizando los datos...")
        self.charge=Progressbar(self.pantalla,mode="indeterminate",maximum=25)
        self.charge.place(x=275,y=225, width=450)
        self.charge.start()
        #Instanciamos otra clase, la del analisis
        print("AQUI SE COMIENZA EL ANALISIS")
        if not os.path.isdir(self.project_path + "/DockingLib"):
            os.makedirs(self.project_path+"/DockingLib/")#Creacion de Directorio para el docking
            os.makedirs(self.project_path+"/models/")
        self.ap = AnalyzeProject(self.project_path)
    
    def change_title(self,text):       #Funcion para cambiar el label de la ventana
        self.r=text     #Define texto
        #time.sleep(duration)    #Define el tiempo (por si se quiere cambiar otra vez)
        self.title.set(self.r)
        self.header.config(text=self.title)
    
    def charge_results(self):
        ##compounds=['Salbutamol','Beclomethasone dipropionate','Alprenolol','Lidocaine,Paracetamol','Omeprazole','Loratadine','Ramipril','Piroxicam','Diazepam','Ibuprofen','Morphine','Chlorphenamine','Aspirin','Prednisone','Epinephrine','Amoxicillin','Albendazole']
        ##compoundsMDB1=['Salbutamol','Ramipril','Piroxicam','Diazepam']
        ##compoundsMDB2=['Loratadine','Ramipril''Diazepam']
        ##compoundsMissed=['Amoxicillin','Albendazole']
        ##proteins=['Actin','Collagen','Glutaminyl','Arginine']
        ##P_notfounds=['Actin','Collagen']
        global Compounds
        global Proteins
        global compoundsMDB1
        global compoundsMDB2
        global compoundsMissed
        global P_notfounds
        compounds=Compounds
        proteins=Proteins
        self.current_res = os.path.dirname(__file__)
        self.rel_pathres="Interfaces/"
        self.abs_file_pathres=os.path.join(self.current_res,self.rel_pathres)
        self.Dir_Success="correcto.png"
        self.Dir_Error="error.png"
        self.Dir_Warn="Advertencia.png"
        self.imgE=PhotoImage(file=self.abs_file_pathres+self.Dir_Error)
        self.imgS=PhotoImage(file=self.abs_file_pathres+self.Dir_Success)
        self.imgW=PhotoImage(file=self.abs_file_pathres+self.Dir_Warn)

        self.imE=self.imgE.subsample(70,70)
        self.imS=self.imgS.subsample(100,100)
        self.imW=self.imgW.subsample(100,100)

        ##############Container Compuestos#########
        self.container = Frame(self.pantalla,bg="white")
        self.canvas = Canvas(self.container,bg="white")
        self.scrollbar = Scrollbar(self.container, orient="vertical", command=self.canvas.yview,bg="white")
        self.scrollable_frame = Frame(self.canvas,bg="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set, width=570,bg="white")
        Headers=['Compuestos','Estructura','Descriptores','Bio-Actividad']
        width = 4

        for i in range(len(compounds)+1): #Rows
            for j in range(width): #Columns

                if(i<1):
                    b=Label(self.scrollable_frame,text=Headers[j],fg="black",font=("Helvetica", 16),bg="white", anchor="n")
                    b.grid(row=i, column=j)
                
                else:
                    if(j==0):
                        lss=compounds[i-1]
                        #print(lss)
                        b = Label(self.scrollable_frame, text=lss,bg="white")
                        #print(compounds[i-1])
                        b.grid(row=i, column=j)
                    elif(j==1):
                        if(compounds[i-1] in compoundsMDB1):
                            b =Label(self.scrollable_frame, image=self.imE,bg="white")
                        else:
                            b = tk.Label(self.scrollable_frame, image=self.imS,bg="white")
                        b.grid(row=i, column=j)
                    
                    elif(j==2):
                        if(compounds[i-1] in compoundsMissed):
                            b = Label(self.scrollable_frame, image=self.imE,bg="white")
                        else:
                            b = Label(self.scrollable_frame, image=self.imS,bg="white")
                        b.grid(row=i, column=j)
                        
                    elif(j==3):
                        if(compounds[i-1] in compoundsMDB2):
                            b = Label(self.scrollable_frame, image=self.imE,bg="white")
                        else:
                            b = Label(self.scrollable_frame, image=self.imS,bg="white")
                        b.grid(row=i, column=j)
        self.container.pack()
        self.canvas.pack(side="left", fill="both", expand=True )
        self.scrollbar.pack(side="right", fill="y")
        self.container.place(x=20,y=100)
        #################Container Proteinas###########
        self.containerP = Frame(self.pantalla,bg="white")
        self.canvasP = Canvas(self.containerP,bg="white")
        self.scrollbarP = Scrollbar(self.containerP, orient="vertical", command=self.canvasP.yview, bg="white")
        self.scrollable_frameP = Frame(self.canvasP,bg="white")
        self.scrollable_frameP.bind(
            "<Configure>",
            lambda e: self.canvasP.configure(
                scrollregion=self.canvasP.bbox("all")
            )
        )

        self.canvasP.create_window((0, 0), window=self.scrollable_frameP, anchor="n")
        self.canvasP.configure(yscrollcommand=self.scrollbarP.set, width=250,bg="white")

        wp=2
        HeadP=['Proteina','Estructura']
        for i in range(len(proteins)+1): #Rows
            for j in range(wp): #Columns

                if(i<1):
                    b=Label(self.scrollable_frameP,text=HeadP[j],fg="black",font=("Helvetica", 16),bg="white", anchor="n")
                    b.grid(row=i, column=j)
                
                else:
                    if(j==0):
                        lss=proteins[i-1]
                        #print(lss)
                        b = Label(self.scrollable_frameP, text=lss,bg="white")
                        #print(compounds[i-1])
                        b.grid(row=i, column=j)
                    elif(j==1):
                        if(proteins[i-1] in P_notfounds):
                            b = Label(self.scrollable_frameP, image=self.imE,bg="white")
                        else:
                            b = Label(self.scrollable_frameP, image=self.imS,bg="white")
                        b.grid(row=i, column=j)
                    

            
        self.containerP.pack()
        self.canvasP.pack(side="left", fill="both", expand=True)
        self.scrollbarP.pack(side="right", fill="y")
        self.containerP.place(x=650,y=100)

        ##Buttons
        self.B_Salir = tk.Button(self.pantalla, text="Salir", width=25, anchor="center")
        self.B_Salir.place(x=550, y=400)
        self.B_Analisis = tk.Button(self.pantalla, text="Continuar",command=self.analizeProject, width=25,anchor="center")
        self.B_Analisis.place(x=250, y=400)


    
    def destroy_screen(self):           #Funcion para destruir la ventana
        self.pantalla.destroy()
    
    def ask_check(self):    #Cuando el usuario da click en OK, se vuelve a revisar que se tenga internet
        global isConnected
        global event
        if messagebox.showerror("Error", "Asegurese que se encuentra conectado a internet",parent=self.pantalla):
            isConnected = CheckConnection.check_internet_conn()
            if not isConnected:
                self.ask_check()
            else:
                event.set()
    
    def incomingProcess(self):      #Funcion que permite a la ventana "atender" lo que hacen los hilos
                                    #Asi evitamos que la interfaz se "congele" mientras los hilos trabajan
        while self.queue.qsize():
            try:
                msg = self.queue.get_nowait()       #Existe una cola de mensajes donde los hilos escriben
                print(msg)
                #if msg == 0:        #Error de conexion
                    #self.ask_check()

                if msg == (self.length_compounds + self.length_proteins):    #Si el mensaje es igual al tamaño 
                                                                             #de la suma de los arreglos significa
                                                                             #que los hilos ya terminaron           
                    #print(self.compoundsMDB1)
                    #print(self.compoundsMDB2)
                    #print(self.compoundsMissed)
                    #print(self.P_notfounds)
                    self.search_end()
                    #self.show_results()
            except queue.Empty:
                pass

#CLASE PARA CREAR HILOS Y REALIZAR LAS FUNCIONES DE DESCARGA DE INFORMACION
class ThreadedClient:

    def __init__(self,drugclass,compounds,proteins,project_path,refButton1,refButton2):     #Constructor de la clase
        global dc
        self.queue = queue.Queue()      #Se define la cola de mensajes
        self.compounds = compounds
        self.proteins = proteins
        self.project_path = project_path
        dc = drugclass
        self.length_compounds = len(compounds)
        self.length_proteins = len(proteins)
        self.refButton1 = refButton1
        self.refButton2 = refButton2
        self.master = tk.Toplevel()     #Como se creaba la pantalla en la clase GUISection
        #Parte de los hilos
        self.running = True
        self.compound_threads = list()
        self.protein_threads = list()
        self.g = 0      #Valor que se espera enviar a la cola de mensajes para los compuestos
        self.lock = threading.Lock()
        self.lock2 = threading.Lock()
        compounds=compounds
        proteins=proteins
        #Lista de elementos que no se encontraron
        self.compoundsMissed = []
        #Computed properties available in PubChem
        self.computedProperties = ['MolecularWeight', 'XLogP', 'HBondDonorCount', 'HBondAcceptorCount',
                            'RotatableBondCount', 'ExactMass', 'MonoisotopicMass', 
                            'TPSA', 'HeavyAtomCount', 'Charge', 'Complexity', 'IsotopeAtomCount', 
                            'DefinedAtomStereoCount', 'UndefinedAtomStereoCount', 'DefinedBondStereoCount', 
                            'UndefinedBondStereoCount', 'CovalentUnitCount']
        self.internalQueue = queue.Queue()  #Cola de mensajes para el manejo de el error de conexion
        self.flag = 0

        #Iniciar GUI
        self.gui = GUISection(self.master, self.queue, self.project_path, self.length_compounds, self.length_proteins,self.refButton1,self.refButton2)
        self.gui.showScreen()

        #Llamando a la funcion de los hilos
        self.threads(self.compounds, self.proteins, self.project_path)  
    
    def incomingInternalProcess(self):      #Aqui se maneja cuando un hilo detecta que no hay conexion
                                            #se detiene la ejecucion del main thread
        try:
            internalmsg = self.internalQueue.get_nowait()       
            print(internalmsg)
            if(internalmsg == 'networkerror'):
                print('Solo veras esto 1 vez')
                #isConnected = False
                self.gui.ask_check()
        except queue.Empty:
            pass

    def threads(self, compounds, proteins, project_path):   #Funcion de los hilos        
        global Compounds
        global Proteins
        Compounds=compounds
        Proteins=proteins
        for item in compounds:  #Un hilo por cada elemento del arreglo compounds
            #print(item)
            #time.sleep(0.2)
            get_compound = threading.Thread(target=self.getCompoundsData,args=(item,self.project_path)) #creacion del hilo, argumentos: un solo compuesto y path
            self.compound_threads.append(get_compound)   #agregar hilo a la lista de hilos de compuestos 
            get_compound.start()    #comenzar hilos
        
        #crear hilos para proteinas (proceso equivalente al de compuestos, pero ahora se usan los items del arreglo proteins)
        for item in proteins:
            #print("PROTEINA ENVIADA: " + sitem)
            get_protein = threading.Thread(target=self.connect_PDB,args=(item, self.project_path))
            get_protein.start()
        
        self.periodic_call()        #Llamando a la funcion periodic_call
        self.periodicInternal_call()     
    
    def periodicInternal_call(self):        #Funcion para checar la cola de mensajes
        self.master.after(200, self.periodicInternal_call)  #Cada 200 ms se llama a si misma y llama a incomingProcess
        self.incomingInternalProcess()
        if not self.running:
            # This is the brutal stop of the system.  You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
    
    def periodic_call(self):        #Funcion para checar la cola de mensajes
        self.master.after(200, self.periodic_call)  #Cada 200 ms se llama a si misma y llama a incomingProcess
        self.gui.incomingProcess()      #Aqui se procesa lo que hay en la cola de mensajes
        if not self.running:
            # This is the brutal stop of the system.  You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
    
    def getCompoundsData(self, compound,project_path):        #Funcion para obtener la informacion de los compuestos
        #print(compound)
        #time.sleep(0.2)         #Esta linea ayuda a probar el error de conexion pues a veces las busquedas son muy rapidas
        self.connect_DrugBank(compound,self.project_path)
        self.connect_DrugBankBA(compound,self.project_path)
        self.connectPubChem(compound,project_path)
        #print('Ya termine la funcion, voy a bloquear')
        self.lock.acquire()      #Cada hilo bloquea el recurso g porque es un valor critico
        self.g += 1         #Se aumenta el valor
        self.lock.release()      #Se libera el recurso
        #print('Ya libere, voy a escribir')
        msg = self.g        #El valor de g se asigna al mensaje que se pondrá en la cola de mensajes
        self.queue.put(msg) #Se envia el mensaje a la cola de mensajes
        return

    
    def connect_DrugBank(self, compounds, project_path):
        #Driver using mozzila to acces a drugbank
        global compoundsMDB1
        global event
        global isConnected

        for attempt in range(3):
            opt=webdriver.ChromeOptions()
            opt.add_argument('headless')
            driveC= webdriver.Chrome(chrome_options=opt)
            #driveC=webdriver.PhantomJS()
            #print(compounds)
            #print(project_path)
            #current_path = os.path.dirname(__file__)
            
                #llamar funcion
                #generararchivo(pathdeaquiabajo, 2)
                #ruta=current_path+"/Compounds/"+compounds[x]+".txt"##Creacion del archivo, String de la ruta
            #print(compounds)
            ruta=project_path+"/Compounds/c0"+compounds+".pdb"##Creacion del archivo, String de la rutaruta=project_path+"/Compounds/c0"+compounds+".pdb"   
                #print(ruta)
            try:

                driveC.get('https://www.drugbank.ca/')
                inputNCom=driveC.find_element_by_id('query')#Explication to manager websites 
                                                                    #actions in https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08
                inputNCom.send_keys(compounds)
                inputNCom.send_keys(Keys.ENTER)
                if ("https://www.drugbank.ca/unearth"  in driveC.current_url):
                    

                    compoundsMDB1.append(compounds)
                    driveC.close()
                    break
                 

                else:
                    #print("Si entro")
                    struct_Down=driveC.find_element_by_xpath('//*[@id="structure-download"]/div/a[4]').get_attribute('href')#Se consigue
                
                    r=requests.get(str(struct_Down))
                    if r.status_code == 200:
                        #print("Qu onda")
                        filet=open(ruta,"tw")
                        filet.write(compounds)
                        filet.write("\nSTRUCTURE:\n")
                        filet.write(r.text)
                        filet.write("##########\n")
                        if compounds in compoundsMDB1:
                            compoundsMDB1.remove(compounds)
                            
                        if compounds not in RealCompounds:
                            RealCompounds.append(compounds)
                        break
                       
                    else:
                        #compoundsMissed.append(compounds)
                        #Error de CONEXION EN LA ESTRUCTURA 
                        print("Error de conexion drugbank")
                        self.lock2.acquire()
                        if isConnected:
                            isConnected = False
                            internalmsg = 'networkerror'
                            self.internalQueue.put(internalmsg)
                        self.lock2.release()
                        event.wait()
                        continue

            except:##ERROR DE CONEXION PARA ESTRUCTURA
                driveC.close()
                print("Error de conexion Drugbank")
                self.lock2.acquire()
                if isConnected:
                    isConnected = False
                    internalmsg = 'networkerror'
                    self.internalQueue.put(internalmsg)
                self.lock2.release()
                event.wait()
                continue
        #call pubChem
        #dataPubChem = threading.Thread(target=connectPubChem, args=(compounds,project_path))
        #dataPubChem.start()
        #print('Check')
    ########################################################################################
    #############################Conexion a DrugBank BA###########################################
    def connect_DrugBankBA(self, compounds, project_path):
        #Driver using mozzila to acces a drugbank
        #x=0
        #compoundsMDB2=[]
        global compoundsMDB2
        global event
        global isConnected
        for attempt in range(3):
            opt=webdriver.ChromeOptions()
            opt.add_argument('headless')
            driveC= webdriver.Chrome(chrome_options=opt)
            
            #ruta=project_path+"/Compounds/c0"+compounds+".txt"##Creacion del archivo, String de la ruta
            ruta=project_path+"/Compounds/c0"+compounds+".pdb"   
            try:    
                driveC.get('https://www.drugbank.ca/')
                inputNCom=driveC.find_element_by_id('query')#Explication to manager websites 
                                                                #actions in https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08
                inputNCom.send_keys(compounds)
                inputNCom.send_keys(Keys.ENTER)
            
                if ("https://www.drugbank.ca/unearth"  in driveC.current_url):
                    
                    if isConnected:
                        compoundsMDB2.append(compounds)
                        driveC.close()
                        break

                else:
                    driveC.implicitly_wait(5)
                    #tableBA=driveC.find_element_by_tag_name("table")
                    #files=tableBA.find_elements_by_tag_name("tr")
                    #tbdy=driveC.find_element_by_xpath('//*[@id="drug-moa-target-table"]')
                    #table=driveC.find_element_by_id("drug-moa-target-table")
                    try:
                        tds=driveC.find_element_by_xpath('//*[@id="drug-moa-target-table"]/tbody')
                        arr=tds.find_elements_by_tag_name("td")
                        array_p=""
                        filet=open(ruta,"a+")
                        filet.write("BIOACTIVITY:\n")
                        for z in range(len(arr)):
                            #print(arr[z].text)
                            array_p=array_p+arr[z].text+'_'
                            if(((z+1)%3)==0):
                                #print(array_p)
                                filet.write(array_p+"\n")
                                array_p="" 
                        
                    #q=(len(arr))/3
                    #print(q)
                    #print(pinter)
                    #print("finish " + compounds)
                    #print("Table founded:"+str(compounds))
                        filet.write("##########\n")
                        if compounds in compoundsMDB2:
                            compoundsMDB2.remove(compounds)
                        break
                    except:
                        if isConnected:
                            compoundsMDB2.append(compounds)
                            filet=open(ruta,"a+")
                            filet.write("BIOACTIVITY:\n")
                            filet.write("EMPTY:NOT FOUND\n")
                            filet.write("##########\n")
                            break
                        else:
                            continue
                #filet.close()
                #print(table)
            except:#BIOACTIVIDAD NO ENCONTRADA POR ERROR DE CONEXION 
                #compoundsMissed.append(compounds)
                driveC.close()
                print("Error de conexion Drugbank BA")
                self.lock2.acquire()
                if isConnected:
                    isConnected = False
                    internalmsg = 'networkerror'
                    self.internalQueue.put(internalmsg)
                self.lock2.release()
                event.wait()
                continue
            #filet.close()
            #print("NOT FOUND MEDICAMENTO")
            #print("Table not founded:"+str(compounds)) 
    ########################################################################################
    #############################Conexion a PDB###########################################
    def connect_PDB(self, item, project_path):
        #P_notfound=[]
        global P_notfounds
        global event
        global isConnected
        global RealProteins
        for attempt in range(3):
            try:
                RName=""
                RName=getbest(item)
                if(RName.find("402")==-1 & RName.find("403")==-1):
                    print(RName)
                    IDP=getIDPDB(RName)
                    #IDP=item
                    coin=True
                    pdbl = PDBList()
                    pdbl.retrieve_pdb_file(IDP, pdir=project_path+"/Proteins", file_format='pdb')
                    sl=IDP.lower()
                    nombre_nuevo=project_path+"/Proteins/cP"+item+".pdb"
                    archivo=project_path+"/Proteins/pdb"+sl+".ent"
                    os.rename(archivo, nombre_nuevo)
                    time.sleep(1) 
                    filet=open(nombre_nuevo,"r+")
                    contenido = filet.read()
                    filet.seek(0, 0)
                    filet.write(item+ '\n' + contenido)
                    if item in P_notfounds:
                        P_notfounds.remove(item)
                    if item not in RealProteins:
                        RealProteins.append(item)    
                    break
                #elif(RName.find(403)==0):
                #    print("Compuesto no encontrado por error de conexion")#Aqui va el error de conexion para el primer request
                #    P_notfounds.append(item) 
                else:
                    print("Compuesto no encontrado por inexistencia")
                    P_notfounds.append(item)
                    
                    

            except:
                    #if(pdbl=="Desired structure doesn't exists"):
                    #    print("PDB no encontrado")
                    #else:
                    print("Error de conexion PDB")#Este capta el error de request para el ID y para el pdbfile
                    self.lock2.acquire()
                    if isConnected:
                        isConnected = False
                        internalmsg = 'networkerror'
                        self.internalQueue.put(internalmsg)
                    self.lock2.release()
                    event.wait()
                    continue
                    #P_notfounds.append(item)

        self.lock.acquire()      #Cada hilo bloquea el recurso g porque es un valor critico
        self.g += 1              #Se aumenta el valor
        self.lock.release()      #Se libera el recurso
        msg = self.g             #El valor de g se asigna al mensaje que se pondrá en la cola de mensajes
        self.queue.put(msg)      #Se envia el mensaje a la cola de mensajes
        #break

        print("Finish ENFERMEDAD")
        return

    #Funcion para obtener datos de Pubchem
    def connectPubChem(self, compounds, project_path):
        #Looking for each compound
        global compoundsMissed      #Este es el arreglo global de los compuestos no encontrados en PubChem
        compoundFounded = ''        #Esta es la variable que indica si existe el compuesto o no
        #c = pcp.get_compounds(compounds, 'name')
        
        #Esta parte es para verificar si el nombre proporcionado existe en la base de datos
        c = self.getValues_PubChem('names', compounds)
        
        if c == []:     #Si el valor es vacio, significa que el compuesto no existe en PubChem
            compoundsMissed.append(compounds)   #Agregamos a compuestos no encontrados
        else:           #Si el valor retorna un ID (identificador del compuesto en la base de datos)
            compoundFounded = compounds #El compuesto si existe, configuramos la variable compoundFounded
                                        #con el nombre del compuesto

        #for each compound founded, try to retrieve its properties
        #Computed properties
        if compoundFounded:             #Si compoundFounded no es una cadena vacia, buscamos las propiedades(descriptores)
            ruta = project_path + "/Compounds/c0" + compoundFounded +".pdb"     #Definimos la ruta del archivo donde vamos a escribir
            #Llamamos a la funcion que conseguira las propiedades del compuesto, y le pasamos el compuesto en cuestión
            p = self.getValues_PubChem('props', compoundFounded)
            #p = pcp.get_properties(self.computedProperties, compoundFounded, 'name')
            
            #Nos retorna un arreglo de objetos con un solo objeto (el compuesto en formato JSON)
            for i in p:     #iteramos en el arreglo (solo es una vez porque solo hay un elemento)
                del i['CID']    #La primera parte del JSON lleva el ID del compuesto, lo eliminamos porque
                                #eso no lo ocupamos cuando escribimos el conjunto cero
                with open(ruta, 'a+') as file:  #Abrimos el archivo y especificamos que vamos a agregar lineas
                    file.write("DESCRIPTORS:\n")  #escribimos
                    json.dump(i, file, sort_keys=True, indent = 2)  #COn esto escribimos el JSON al conjunto 0 del compuesto
                    file.write("\n##########\n")    #escribimos
                    file.write("FINAL")             #escribimos

            #print("Ya busque las propiedades " + compoundFounded)

        """self.lock.acquire()      #Cada hilo bloquea el recurso g porque es un valor critico
        self.g += 1         #Se aumenta el valor
        self.lock.release()      #Se libera el recurso
        msg = self.g        #El valor de g se asigna al mensaje que se pondrá en la cola de mensajes
        self.queue.put(msg) #Se envia el mensaje a la cola de mensajes"""
    
    #@sleep_and_retry
    #@limits(calls = 5, period = 1.2)
    def getValues_PubChem(self, case, compoundToSearch):
        value = []      #definimos un arreglo que sera lo que retorne al final esta funcion
        global event    #el evento es global y sirve para controlar la pausa de los hilos (cuando no hay conexion)
        global isConnected

        for attemp in range(3):     #se intentara 3 veces llamar a la API (mecanismo retry)
            try:            
                if case == 'names':     #si se llamo para verificar que el compuesto existe
                    #print('caso names')
                    value = pcp.get_compounds(compoundToSearch, 'name') #llamamos a la API con pubchempy

                elif case == 'props':   #SI se llamo para obtener las propiedades de un compuesto
                    #print('caso props')
                    value = pcp.get_properties(self.computedProperties, compoundToSearch, 'name')   #llamamos a la API
                break   #Si llega hasta aca es porque si termino la funcion correctamente, rompe el ciclo FOR

            except pcp.PubChemHTTPError:        #Este es el error que arroja si haces mas de 5 peticiones por segundo
                print('SERVER BUSY')
                time.sleep(1)                   #dormimos ese hilo un segundo
                continue                        #volvemos a intentar (este continue le dice al for que vaya a la siguiente iteracion y vuelve
                                                #a hacer el try)

            except urllib.error.URLError: #Error: Name or service not known
                """internalmsg = 0
                self.queue.put(internalmsg)
                event.wait()
                continue"""
                self.lock2.acquire()
                print('Error de conexion: Pubchem')
                if isConnected:
                    isConnected = False
                    internalmsg = 'networkerror'
                    self.internalQueue.put(internalmsg)
                self.lock2.release()
                event.wait()
                continue
                """if self.flag < 1:
                    self.lock2.acquire()
                    self.flag += 1
                    self.lock2.release()
                    internalmsg = 'networkerror' + str(self.flag)
                    self.internalQueue.put(internalmsg)
                    event.wait()
                    continue
                else:
                    event.wait() 
                    continue"""

        return value

class AnalyzeProject:
    def __init__(self, project_path):
        global dc
        #AQUI YA ESTA PUESTA LA PANTALLA DE ANALISIS DE DATOS, COMENZAR DOCKING
        #Para programarlo se debe utilizar multiproceso
        #PRIMERO, verificar si ya existe el archivo de coeficientes
        self.flag = False
        self.project_path = project_path
        self.drugclass = dc
        self.deltaG = []    #Arreglo para guardar los valores de las delta G que arroja el docking
        self.coefs = []     #Arreglo donde se guardan los coeficientes en caso de que ya existan
        self.lookForValues()
    
    def lookForValues(self):
        #leer en el directorio a ver si existe el archivo que corresponde a la linea del archivo inicial
        #que identifica la clase de medicamentos que se estan analizando
        print(self.drugclass)
        modelDir = self.project_path + '/models'
        """
        try:
            with open(os.path.join(self.project_path,'values.txt')) as f:
                #Buscar la etiqueta que corresponde a la clase del archivo
                for line in f:
                    if line.strip() == self.drugclass:
                        #print('en el archivo ya encontre el valor')
                        self.flag = True
                    if self.flag:
                        #Setear valores de los coeficientes en un arreglo
                        if line.strip() == '##########':
                            break
                        else:
                            self.coefs.append(line.rpartition(':')[2])
            
            if not self.flag:   #El archivo existe pero no se ha registrado los valores para
                            #La clasificacion de medicamentos indicada, hay que hacer docking
                print('El archivo existe pero no hay info adecuada')
                self.processDocking()
            else:               #Ya existen los coeficientes, solo resolver ecuación lineal
                print('Ya existen los coeficientes')
                self.simpleSolution()

        except FileNotFoundError:
            #No existe un archivo con los valores, se debe hacer docking
            print('No se encontro el archivo')
            self.processDocking()"""
        for f in os.walk(modelDir):
            if f == self.modelFile:
                #El modelo ya existe
                print('El modelo ya existe')
                self.simpleSolution()
                break
        else:
            #El modelo no existe
            print('EL modelo no existe')
            self.processDocking()
    
    def processDocking(self):
        Compounds_1 = []
        Proteins_1 = []
        global RealCompounds
        global RealProteins
        full_path = self.project_path #Path donde se guarda la carpeta Compounds y Proteins
        
        for contador_prueba in RealCompounds:
            compuesto_com = 'c0' + contador_prueba
            Compounds_1.append(compuesto_com)
        
        for contador_prueba1 in RealProteins:
            proteina_com = 'cP' + contador_prueba1
            Proteins_1.append(proteina_com)
        
        # ------------------------- Paths ----------------------- #
        Compounds_path = '../Compounds'
        Proteins_path = '../Proteins'
        Path_Libreria = full_path + '/DockingLib'
        Path_PDBQT = Path_Libreria + '/PDBQT'

        # ---------------- Guardamos archivos de las librerias --------------- #
        path_obtener_libreria = '/usr/local/bin'
        os.chdir(path_obtener_libreria)
        copiar = 'cp /usr/local/bin/prepare_ligand4.py prepare_receptor4.py prepare_gpf4.py pythonsh ' + Path_Libreria
        os.system(copiar)

        # ------------------ Comandos para crear ligandos y receptores ----------------------- #
        ligand = './pythonsh prepare_ligand4.py -l '
        receptor = './pythonsh prepare_receptor4.py -r '
        gpf = './pythonsh prepare_gpf4.py -l '
        # --------- Diccionario donde se guardaran las deltas --------------- #
        Deltas = {}
        # --------- Proceso de docking --------------- #
        os.chdir(Path_Libreria)
        if os.path.isdir(Path_PDBQT):
            print("La carpeta exite")
        else:
            os.mkdir('PDBQT')
        # ---------- Creando los archivos ligando ----------- #
        for contador_com in Compounds_1:
            for contador_pro in Proteins_1:
                os.chdir(Path_PDBQT)
                Protein_Compound = contador_pro + '_' + contador_com
                Path_Compuesto_Proteina = Path_PDBQT + '/' + Protein_Compound
                # ----------------- Creamos el directorio----------- #
                if os.path.isdir(Path_Compuesto_Proteina):
                    Archivo_check = Path_Compuesto_Proteina + '/' + contador_pro + '.pdbqt'
                    os.chdir(Path_Compuesto_Proteina)
                    if os.path.isfile(Archivo_check):
                        print("Archivo existe")
                    else:
                        os.chdir(Path_Libreria)
                        comando_receptor = receptor + Proteins_path + '/' + contador_pro + '.pdb -o ' + 'PDBQT' + '/' + Protein_Compound +'/' + contador_pro + '.pdbqt'
                        os.system(comando_receptor)
                    Archivo_check = Path_Compuesto_Proteina + '/' + contador_com + '.pdbqt'
                    os.chdir(Path_Compuesto_Proteina)
                    if os.path.isfile(Archivo_check):
                        print("Archivo existe")
                    else:
                        os.chdir(Path_Libreria)
                        comando_ligan = ligand + Compounds_path + '/' + contador_com + '.pdb -o' + 'PDBQT' + '/' + Protein_Compound + '/' + contador_com + '.pdbqt'
                        os.system(comando_ligan)
                else:    
                    os.mkdir(Protein_Compound)
                    os.chdir(Path_Libreria)
                    comando_receptor = receptor + Proteins_path + '/' + contador_pro + '.pdb -o ' + 'PDBQT' + '/' + Protein_Compound +'/' + contador_pro + '.pdbqt'
                    os.system(comando_receptor)
                    comando_ligan = ligand + Compounds_path + '/' + contador_com + '.pdb -o' + 'PDBQT' + '/' + Protein_Compound + '/' + contador_com + '.pdbqt'
                    os.system(comando_ligan)
                #-------- Archivo gpf ----------- #
                os.chdir(Path_Compuesto_Proteina)
                Archivo_check = Path_Compuesto_Proteina + '/' + Protein_Compound + '.gpf'
                if os.path.isfile(Archivo_check):
                    print("Archivo existe")
                else:
                    os.chdir(Path_Libreria)
                    comando_gpf = gpf + 'PDBQT/'+ Protein_Compound + '/'+ contador_com +'.pdbqt -r ' + 'PDBQT/'+ Protein_Compound + '/'+ contador_pro + '.pdbqt -o '+'PDBQT/'+ Protein_Compound +'/'+ Protein_Compound + '.gpf'
                    os.system(comando_gpf)
                # ------ Coordenadas del centro -------- #
                os.chdir(Path_Compuesto_Proteina)
                Archivo_check = Path_Compuesto_Proteina + '/' + contador_pro + '.A.map'
                if os.path.isfile(Archivo_check):
                    # ----------- Obtener coordenadas ------------ #
                    Palabra = 'CENTER'
                    archivo = contador_pro + '.A.map'
                    file = open(archivo, "r")
                    while(True):
                        linea = file.readline()
                        if Palabra in linea:
                            coordenada = linea
                            break
                        if not linea:
                            break
                    file.close()
                    coordenadas = coordenada.split()
                else:
                    try:
                        os.chdir(Path_Compuesto_Proteina)
                        comando_autogrid = 'autogrid4 -p '+ Protein_Compound + '.gpf'
                        os.system(comando_autogrid)
                        # ---------- Obtener coordenadas ---------------#
                        Palabra = 'CENTER'
                        archivo = contador_pro + '.A.map'
                        file = open(archivo, "r")
                        while(True):
                            linea = file.readline()
                            if Palabra in linea:
                                coordenada = linea
                                break
                            if not linea:
                                break
                        file.close()
                        coordenadas = coordenada.split()
                    except:
                        print("No hay archivos .gpf")
                # -------- Creación del archivo de config ----- #
                Archivo_check = Path_Compuesto_Proteina + '/' + 'config.txt'
                if os.path.isfile(Archivo_check):
                    Archivo_check = Path_Compuesto_Proteina + '/' + Protein_Compound + '.pdbqt'
                    if os.path.isfile(Archivo_check):
                        print("Docking hecho")
                    else:
                        docking = 'vina --config config.txt'
                        os.system(docking)
                else:
                    try:
                        recep = 'receptor='+ contador_pro + '.pdbqt\n'
                        ligando = 'ligand=' + contador_com + '.pdbqt\n\n'
                        out = 'out=' + Protein_Compound + '.pdbqt'
                        out2 = Protein_Compound + '.pdbqt'

                        center_x = 'center_x=' + coordenadas[1] + '\n'
                        center_y = 'center_y=' + coordenadas[2] + '\n'
                        center_z = 'center_z=' + coordenadas[3] + '\n\n'

                        configuracion = open("config.txt","w")
                        configuracion.write(recep)
                        configuracion.write(ligando)
                        configuracion.write(center_x)
                        configuracion.write(center_y)
                        configuracion.write(center_z)
                        configuracion.write('size_x=40\nsize_y=40\nsize_z=40\n\n')
                        configuracion.write('exhaustiveness=8\n')
                        configuracion.write('num_modes=9\n')
                        configuracion.write('energy_range=3\n\n')
                        configuracion.write(out)
                        configuracion.close()
                        # ------------- docking ----------- #
                        docking = 'vina --config config.txt'
                        os.system(docking)
                    except:
                        print("No se puede hacer docking")
                # --------- Guardando deltas -----------#
                Palabra = 'REMARK VINA RESULT:'
                Archivo_check = Path_Compuesto_Proteina + '/' + Protein_Compound + '.pdbqt'
                out2 = Protein_Compound + '.pdbqt'
                if os.path.isfile(Archivo_check):
                    file = open(out2,'r')
                    while(True):
                        linea = file.readline()
                        if Palabra in linea:
                            Delta_p = linea.split()
                            Deltas[Protein_Compound] = [float(Delta_p[3])]
                            break
                        if not linea:
                            break
                    file.close()
                    
        Deltas_ordenadas = Deltas.items()
        print(Deltas_ordenadas)
        Deltas_tuplas = sorted(Deltas_ordenadas, reverse=True)
        print(Deltas_tuplas)


        #Aqui llamamos para limpiar las tuplas
        #cleanDeltas = self.fixDeltas(Deltas_tuplas)

        #Llamamos a la regresion lineal
        #self.mlAlgorithm(cleanDeltas)
        #Creamos los procesos
        """pool = mp.Pool(mp.cpu_count())
        #Pasar diccionario a lista
        itemsDeltas = list(Deltas_ordenadas.items())

        if len(Deltas_ordenadas) <= mp.cpu_count():
            fixedchunkSize = 1
        else:
            chunkSize = len(Deltas_ordenadas) / mp.cpu_count()
            fixedchunkSize = int(chunkSize)
            residual = int(chunkSize % 2)
            if residual == 0:
                print('Queda exacto')
            else:
                print('No queda exacto')
                fixedchunkSize += residual

        chunk = [itemsDeltas[i:i + fixedchunkSize ] for i in range(0, len(itemsDeltas), fixedchunkSize)]
        coefs = pool.map(mlAlgorithm, chunk)"""

    def fixDeltas(self,deltas):
    #Aqui se hace el fix a las tuplas y se genera un diccionario
        newDict = {}
        counter = 0
        dictCounter = 0
        divisor = {}
        rawCompounds = [item[0] for item in deltas]
        rawDeltas = [item[1] for item in deltas]

        for item in rawCompounds:
            fixCompound = item.rpartition('_')[2]
            if fixCompound in newDict:
                if rawDeltas[counter] < 0:
                    if newDict.get(fixCompound) > 0:
                        newDeltaValue = rawDeltas[counter]
                    else:
                        newDeltaValue = rawDeltas[counter] +  newDict.get(fixCompound)
                        if divisor:
                            for key,value in divisor.items():
                                if key == fixCompound:
                                    value += 1
                                    break
                            else:
                                divisor[fixCompound] = 2 
                        else:
                            divisor[fixCompound] = 2
                else:
                    if rawDeltas[counter] < newDict.get(fixCompound):
                        newDeltaValue = rawDeltas[counter]
                    else:
                        newDeltaValue = newDict.get(fixCompound)

                newDict[fixCompound] = newDeltaValue
            else:
                newDict[fixCompound] = rawDeltas[counter]
            counter += 1
            #print(divisor)
        
        for key in newDict:
            for keys,values in divisor.items():
                if keys == key:
                    fixDivisor = values
                    break
            else:
                fixDivisor = 1

            newDict[key] = round((newDict[key] / fixDivisor), 2)

        #print (newDict)           
        return newDict
    
    def simpleSolution(self):
        global RealCompounds
        print('Solo debes resolver ecuación lineal')

        #AQUI YA ESTAMOS SEGUROS QUE EXISTE UN MODELO CREADO
        loaded_model = pickle.load(open(os.path.join(self.modelPath,self.modelFile), 'rb'))
        toPredict = self.getDescriptors(RealCompounds)
        result = loaded_model.predict(toPredict)
        print(result)
    
    def getDescriptors(self, listofdescriptors):
        descriptors = []
        newDescriptors = []
        for item in listofdescriptors:
            compoundName = 'c0' + item + '.pdb'
            #Acceder al directorio de compounds y buscar ese compuesto
            with open(os.path.join(self.compoundPath, compoundName)) as f:
                for line in f:
                    if '{' in line.strip():
                        for l in f:
                            if l.strip() == '}':
                                break
                            if l.strip().endswith(','):
                                result = re.search(':(.*),', l.strip())
                                #print(result.group(1))
                                descriptors.append(result.group(1))
                            else:
                                r = l.strip().rpartition(':')[2]
                                descriptors.append(r)
                                #print(r)

            #print(descriptors)
            #Convertir valores a flotantes todos
            newDescriptors.append([float(item) for item in descriptors])
            del descriptors[:]

        #print(newDescriptors)

            #Pasar los valores a formato pandas
        descriptorsDataFrame = pd.DataFrame(newDescriptors, columns=['MolecularWeight', 'XLogP', 'HBondDonorCount', 'HBondAcceptorCount',
                                'RotatableBondCount', 'ExactMass', 'MonoisotopicMass', 
                                'TPSA', 'HeavyAtomCount', 'Charge', 'Complexity', 'IsotopeAtomCount', 
                                'DefinedAtomStereoCount', 'UndefinedAtomStereoCount', 'DefinedBondStereoCount', 
                                'UndefinedBondStereoCount', 'CovalentUnitCount'])
        
        return descriptorsDataFrame
    
    def mlAlgorithm(self,deltas):
        print('Aqui debemos implementar la regresion lineal')
        descriptors = []
        newDescriptors = []
        compoundPath = self.project_path + '/Compounds'
        rawNames = list(deltas.keys())
        for item in rawNames:
            compoundName = item.rpartition('_')[2]
            compoundName = 'c0' + compoundName + '.pdb'
            #Acceder al directorio de compounds y buscar ese compuesto
            with open(os.path.join(compoundPath, compoundName)) as f:
                for line in f:
                    if '{' in line.strip():
                        for l in f:
                            if l.strip() == '}':
                                break
                            if l.strip().endswith(','):
                                result = re.search(':(.*),', l.strip())
                                #print(result.group(1))
                                descriptors.append(result.group(1))
                            else:
                                r = l.strip().rpartition(':')[2]
                                descriptors.append(r)
                                #print(r)

            #print(descriptors)
            #Convertir valores a flotantes todos
            newDescriptors.append([float(item) for item in descriptors])
            del descriptors[:]

        #print(newDescriptors)

            #Pasar los valores a formato pandas
        descriptorsDataFrame = pd.DataFrame(newDescriptors, columns=['MolecularWeight', 'XLogP', 'HBondDonorCount', 'HBondAcceptorCount',
                                'RotatableBondCount', 'ExactMass', 'MonoisotopicMass', 
                                'TPSA', 'HeavyAtomCount', 'Charge', 'Complexity', 'IsotopeAtomCount', 
                                'DefinedAtomStereoCount', 'UndefinedAtomStereoCount', 'DefinedBondStereoCount', 
                                'UndefinedBondStereoCount', 'CovalentUnitCount'])

        print(descriptorsDataFrame)

        #print(descriptorsDataFrame)
        listDeltas = list(deltas.values())
        deltasDataFrame = pd.DataFrame(listDeltas, columns=['delta'])
        #print(deltasDataFrame)
            #Aplicar regresion
        regressor = LinearRegression() 
        regressor.fit(descriptorsDataFrame, deltasDataFrame)

        #Obtener coeficientes
        print(regressor.coef_)
        #coeffs = pd.DataFrame(regressor.coef_, descriptorsDataFrame.columns, columns=['Coefficient'])
        #Guardamos el modelo pra futuras predicciones
        pickle.dump(regressor, open(os.path.join(self.modelPath,self.modelFile), 'wb'))
        #Tambien se debe guardar los datos de la regresion en un diccionario y CREAR y escribirlos
        #al archivo values en el formato:
        #drugclass
        #x1:a
        #x2:b
