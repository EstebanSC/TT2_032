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
import requests
import os
from pypdb import find_results_gen
import time
from ratelimit import limits, sleep_and_retry

#Definicion de la pantalla descargas
isConnected = True                  #Esta es una condicion que se estara checando cuando se hagan
                                    #las llamadas a las API o se use internet. Es True puesto que
                                    #First_S.py ya se checo el internet y si esta aqui es por que si hay
event = threading.Event()
#COmpuestos o proteinas no encontrados
compoundsMDB1=[]#Compuestos Perdidos DB1
compoundsMDB2=[]#Compuesto Perdidos DB2
P_notfounds=[] #Proteinas Perdidas
compoundsMissed=[] #Compuestos Pub
class GUISection:

    def __init__(self, master, queue, lenCompounds, lenProteins,refButton1,refButton2):      #Constructor de la clase
        current_path = os.path.dirname(__file__) # Where your .py file is located
        self.queue = queue
        self.pantalla = master
        self.length_compounds = lenCompounds
        self.length_proteins = lenProteins
        #self.project_path = project_path
        self.refButton1 = refButton1
        self.refButton2 = refButton2
        self.pantalla.resizable(False, False)
        self.pantalla.protocol("WM_DELETE_WINDOW", self.ask_quit)
        self.telacontrol=Canvas(self.pantalla,height=450,width=850,bg="white" )
        self.telacontrol.pack(expand=FALSE)
        self.title=tk.StringVar()
        self.r="Buscando datos..."
        self.title.set(self.r)
        self.header=Label(self.pantalla,textvariable=self.title,bg="white",anchor=N)
        self.header.configure(font=("Arial Black",26))
        #self.header.config(anchor=CENTER)
        self.header.pack()
        self.charge=Progressbar(self.pantalla,mode="indeterminate",maximum=25)
        #self.charge.pack()    

    def showScreen(self):       #Funcion para mostrar la pantalla
        self.pantalla.title("Busqueda")
        self.pantalla.geometry("850x450")
        CenterScreen.center_screen(self.pantalla)
        self.header.place(x=25,y=50)
        self.charge.place(x=250,y=250, width=350)
        self.charge.start()
        #time.sleep(3)
       
    def ask_quit(self):         #Funcion para el cuadro de dialogo que permita cerrar la ventana
        if messagebox.askokcancel("Cerrar", "Desea cerrar la busqueda de datos ?",parent=self.pantalla):
            self.refButton1["state"] = ["normal"]
            self.refButton2["state"] = ["normal"]
            self.pantalla.destroy()

    #NOTA: ESTO ES UNA FUNCION PARA PRUEBAS VISUALES
    def search_end(self):
        #self.change_title("Finalizando busqueda...",2)
        #self.change_title("Recopilando resultados...",3)
       
        self.change_title("RESULTADOS DE LA BUSQUEDA")
        self.charge.destroy()
        
    
    def change_title(self,text):       #Funcion para cambiar el label de la ventana
        self.r=text     #Define texto
        #time.sleep(duration)    #Define el tiempo (por si se quiere cambiar otra vez)
        self.title.set(self.r)
        self.header.config(text=self.title)
    
    def destroy_screen(self):           #Funcion para destruir la ventana
        self.pantalla.destroy()
    
    def ask_check(self):    #Cuando el usuario da click en OK, se vuelve a revisar que se tenga internet
        global isConnected
        global event
        if messagebox.showerror("Revisar conexion", "Asegurese que se encuentra conectado a internet",parent=self.pantalla):
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

    def __init__(self,compounds,proteins,project_path,refButton1,refButton2):     #Constructor de la clase
        self.queue = queue.Queue()      #Se define la cola de mensajes
        self.compounds = compounds
        self.proteins = proteins
        self.project_path = project_path
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
        self.gui = GUISection(self.master, self.queue, self.length_compounds, self.length_proteins,self.refButton1,self.refButton2)
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
        #compoundsMDB1=[]
        global compoundsMDB1
        global event
        global isConnected

        opt=webdriver.ChromeOptions()
        opt.add_argument('headless')
        driveC= webdriver.Chrome(chrome_options=opt)
        #driveC=webdriver.PhantomJS()
        #print(compounds)
        #print(project_path)
        current_path = os.path.dirname(__file__)
        
            #llamar funcion
            #generararchivo(pathdeaquiabajo, 2)
            #ruta=current_path+"/Compounds/"+compounds[x]+".txt"##Creacion del archivo, String de la ruta
        #print(compounds)
        ruta=project_path+"/Compounds/c0"+compounds+".txt"##Creacion del archivo, String de la ruta
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
            else:

                struct_Down=driveC.find_element_by_xpath('//*[@id="structure-download"]/div/a[4]').get_attribute('href')#Se consigue
            
                r=requests.get(str(struct_Down))
                if r.status_code == 200:
                    filet=open(ruta,"tw")
                    filet.write(compounds)
                    filet.write("\nSTRUCTURE:\n")
                    filet.write(r.text)
                    filet.write("##########\n")
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
                driveC.close()

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

        opt=webdriver.ChromeOptions()
        opt.add_argument('headless')
        driveC= webdriver.Chrome(chrome_options=opt)
        
        ruta=project_path+"/Compounds/c0"+compounds+".txt"##Creacion del archivo, String de la ruta
        try:    
            driveC.get('https://www.drugbank.ca/')
            inputNCom=driveC.find_element_by_id('query')#Explication to manager websites 
                                                            #actions in https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08
            inputNCom.send_keys(compounds)
            inputNCom.send_keys(Keys.ENTER)
        
            if ("https://www.drugbank.ca/unearth"  in driveC.current_url):
                compoundsMDB2.append(compounds)
                driveC.close()
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
                except:
                    compoundsMDB2.append(compounds)
                    filet=open(ruta,"a+")
                    filet.write("BIOACTIVITY:\n")
                    filet.write("EMPTY:NOT FOUND\n")
                    filet.write("##########\n")
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
                #P_notfounds.append(item)

        self.lock.acquire()      #Cada hilo bloquea el recurso g porque es un valor critico
        self.g += 1              #Se aumenta el valor
        self.lock.release()      #Se libera el recurso
        msg = self.g             #El valor de g se asigna al mensaje que se pondrá en la cola de mensajes
        self.queue.put(msg)      #Se envia el mensaje a la cola de mensajes

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
            ruta = project_path + "/Compounds/c0" + compoundFounded +".txt"     #Definimos la ruta del archivo donde vamos a escribir
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