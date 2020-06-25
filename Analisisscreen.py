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
import CenterScreen
#Imports para los hilos
import threading
import queue as queue
import time
from ratelimit import limits, sleep_and_retry
import multiprocessing as mp
import pandas as pd
import operator
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split
import numpy as np 
import pickle
#import subprocess
from pathlib import Path
import Resultados

class GUISection:
    def __init__(self,master):
        self.PantallaA=master
        self.PantallaA.resizable(False,False)
        self.PantallaA.protocol("WM_DELETE_WINDOW", self.ask_quit)
        self.telacontrol=Canvas(self.PantallaA,height=450,width=950,bg="white" )
        self.telacontrol.pack(expand=FALSE)
        self.title=tk.StringVar()
        self.r="Analizando datos..."
        self.title.set(self.r)
        self.header=Label(self.PantallaA,textvariable=self.title,bg="white", anchor="n")
        self.header.configure(font=("Arial Black",26))
        #self.header.config(anchor=CENTER)
        self.header.pack()
        self.charge=Progressbar(self.PantallaA,mode="indeterminate",maximum=25)
        self.charge.pack()

    def showScreen(self):       #Funcion para mostrar la pantalla
        self.PantallaA.title("Análisis")
        self.PantallaA.geometry("950x450")
        #self.pantalla.title("Búsqueda")
        #self.pantalla.geometry("850x450")
        CenterScreen.center_screen(self.PantallaA)
        self.header.place(x=325,y=25)
        self.charge.place(x=275,y=225, width=450)
        self.charge.start()
    
    def ask_quit(self):         #Funcion para el cuadro de dialogo que permita cerrar la ventana
        if messagebox.askokcancel("Cerrar", "¿Desea cerrar el análisis de datos?",parent=self.PantallaA):
        #if messagebox.askokcancel("Cerrar", "¿Desea cerrar la búsqueda de datos?",parent=self.pantalla):
            self.PantallaA.destroy()

    def callDestroy(self):
       self.PantallaA.destroy()
    
class ThreadAnlisis:

    def __init__(self,project_path,dc,RealCompounds,RealProteins,dockingOption,dockCompounds,dockProteins):
        self.running=True
        self.master=tk.Toplevel()
        self.gui=GUISection(self.master)
        #verS=threading.Thread(target=self.gui.showScreen)
        self.gui.showScreen()
        #verS.start()
        self.flag = False
        self.project_path = project_path
        self.compoundPath = project_path + '/Compounds'
        self.drugclass = dc
        self.modelPath = str(Path.home()) + "/models"   #Esto se debe cambiar
        self.modelFile = dc + '.sav'
        self.deltaG = []    #Arreglo para guardar los valores de las delta G que arroja el docking
        self.coefs = []     #Arreglo donde se guardan los coeficientes en caso de que ya existan
        self.RealCompounds=RealCompounds
        self.RealProteins=RealProteins
        self.dockingOption=dockingOption
        self.dockProteins=dockProteins
        self.dockCompounds=dockCompounds
        #time.sleep(10)
        Mero=threading.Thread(target=self.lookForValues)
        #self.lookForValues()
        Mero.start()

    def lookForValues(self):
        #leer en el directorio a ver si existe el archivo que corresponde a la linea del archivo inicial
        #que identifica la clase de medicamentos que se estan analizando
        if self.dockingOption:
            self.RealCompounds = self.dockCompounds.copy()
            self.RealProteins = self.dockProteins.copy()
        print(self.drugclass)
        for root,dirs,files in os.walk(self.modelPath):
            if self.drugclass in dirs:
                print('El modelo ya existe')
                for root,dirs,files in os.walk(self.modelPath + '/' + self.drugclass):
                    if ('desc' + self.drugclass + '.txt') in files:
                        with open(os.path.join((self.modelPath + '/' + self.drugclass),('desc' + self.drugclass + '.txt')), 'r') as f:
                            for line in f:
                                r = line.strip().rpartition(':')[0]
                                print(r)
                                v = line.strip().rpartition(':')[2]
                                print(v)
                                if r == 'Size':
                                    if (int(v) - len(self.RealCompounds)) > 0:
                                        print('Voy a SOLUTION')
                                        self.simpleSolution()
                                        break
                                    else:
                                        print('VOY A DOCKING')
                                        self.processDocking()
                                        break
                        break
                break
        else:
            #El modelo no existe
            print('EL modelo no existe')
            self.processDocking()

    def processDocking(self):
        if not os.path.isdir(self.project_path + "/DockingLib"):
            os.makedirs(self.project_path+"/DockingLib/")#Creacion de Directorio para el docking
        Compounds_1 = []
        Proteins_1 = []
        #self.RealCompounds
        #global RealProteins
        #global dockingOption
        
        if self.dockingOption:
            #global dockCompounds
            #global dockProteins
            self.RealCompounds = self.dockCompounds.copy()
            self.RealProteins = self.dockProteins.copy()
         
        full_path = self.project_path #Path donde se guarda la carpeta Compounds y Proteins
        
        for contador_prueba in self.RealCompounds:
            compuesto_com = 'c0' + contador_prueba
            Compounds_1.append(compuesto_com)
        
        for contador_prueba1 in self.RealProteins:
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
                    print(Archivo_check)
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
                        #CPU_check = subprocess.check_output(['nproc', '--all'])
                        #CPU_1 = int(CPU_check)
                        #CPU = 'cpu=' + str(CPU_1) + '\n'

                        configuracion = open("config.txt","w")
                        configuracion.write(recep)
                        configuracion.write(ligando)
                        configuracion.write(center_x)
                        configuracion.write(center_y)
                        configuracion.write(center_z)
                        configuracion.write('size_x=40\nsize_y=40\nsize_z=40\n\n')
                        #configuracion.write(CPU)
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
                            Deltas[Protein_Compound] = float(Delta_p[3])
                            break
                        if not linea:
                            break
                    file.close()

        """for key,value in Deltas:
            fixValue = value[0]
            value = fixValue """  
        Deltas_ordenadas = Deltas.items()
        #print(Deltas_ordenadas)
        Deltas_tuplas = sorted(Deltas_ordenadas, reverse=True)
        #print(Deltas_tuplas)
        Deltas_ordenadas = Deltas.items()
        #print(Deltas_ordenadas)
        Deltas_tuplas = sorted(Deltas_ordenadas, reverse=True)
        #print(Deltas_tuplas)


        #Aqui llamamos para limpiar las tuplas
        self.cleanDeltas = self.fixDeltas(Deltas_tuplas)

        #Llamamos a la regresion lineal
        self.mlAlgorithm(self.cleanDeltas)
     

    def simpleSolution(self):
        #global RealCompounds
        simpleDict = {}
        if self.dockingOption:
            #self.dockCompounds
            self.RealCompounds = self.dockCompounds.copy()
        
        print('Solo voy a resolver la ecuacion')

        #AQUI YA ESTAMOS SEGUROS QUE EXISTE UN MODELO CREADO
        comps = self.getDescriptors(self.RealCompounds)
        #print(comps)
        fixModelPath = self.modelPath + '/' + self.drugclass
        loaded_model = pickle.load(open(os.path.join(fixModelPath,self.modelFile), 'rb'))
        result = loaded_model.predict(comps)

        print(result)
        for index,item in enumerate(self.RealCompounds):
            item = 'c0' + item
            result[index][0] = round(result[index][0], 2)
            simpleDict[item] = result[index][0]
        print(simpleDict)

        FinalScreen = Resultados.Resultados(simpleDict,self.project_path)
        self.gui.callDestroy()
        print('Ya resolvi el modelo predictivo')
        #print(result)
    
    def getDescriptors(self, listofdescriptors):
        #print(listofdescriptors)
        descriptors = []
        newDescriptors = []
        for item in listofdescriptors:
            compoundName = 'c0' + item + '.pdb'
            #Acceder al directorio de compounds y buscar ese compuesto
            try:
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
                newDescriptors.append([float(item) for item in descriptors])
                del descriptors[:]

            except FileNotFoundError:
                pass
            #print(descriptors)
            #Convertir valores a flotantes todos

        #print(newDescriptors)

            #Pasar los valores a formato pandas
        descriptorsDataFrame = pd.DataFrame(newDescriptors, columns=['MolecularWeight', 'XLogP', 'HBondDonorCount', 'HBondAcceptorCount',
                                'RotatableBondCount', 'ExactMass', 'MonoisotopicMass', 
                                'TPSA', 'HeavyAtomCount', 'Charge', 'Complexity', 'IsotopeAtomCount', 
                                'DefinedAtomStereoCount', 'UndefinedAtomStereoCount', 'DefinedBondStereoCount', 
                                'UndefinedBondStereoCount', 'CovalentUnitCount'])
        
        return descriptorsDataFrame

       
        

    def fixDeltas(self,deltas):
    #Aqui se hace el fix a las tuplas y se genera un diccionario
        print('ENTRE A LIMPIAR')
        print(deltas)
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

        print ("YA LIMPIE LAS DELTAS")
        print(newDict)           
        return newDict  


    def mlAlgorithm(self,deltas):
        print('voy a implementar la regresion')
        descriptors = []
        newDescriptors = []
        compoundPath = self.project_path + '/Compounds'
        rawNames = list(deltas.keys())
        for item in rawNames:
            compoundName = item + '.pdb'
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

        #print(descriptorsDataFrame)

        #print(descriptorsDataFrame)
        listDeltas = list(deltas.values())
        print(listDeltas)
        deltasDataFrame = pd.DataFrame(listDeltas, columns=['delta'])
        X_train, X_test, y_train, y_test = train_test_split(descriptorsDataFrame, deltasDataFrame, test_size=0.2, random_state=0)
        #print(deltasDataFrame)
        print(len(X_train))
            #Aplicar regresion
        regressor = LinearRegression() 
        regressor.fit(X_train, y_train)

        #Obtener coeficientes
        print('YA REALICE LA REGRESION')
        print(regressor.coef_)
        #prediccion
        deltasPred = regressor.predict(X_test)
        print(len(deltasPred))
        #print(deltasPred)
        #print(y_test)
        
        #df = pd.DataFrame({'Actual': y_test.values.flatten(), 'Predicted': deltasPred.values.flatten()})
        #print(df)
        
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, deltasPred))  
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, deltasPred))  
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, deltasPred)))
        fixModelPath = self.modelPath + '/' + self.drugclass
        if not os.path.isdir(fixModelPath):
            os.makedirs(fixModelPath)
        descFile = 'desc' + self.drugclass + '.txt'
        #Guardamos el modelo pra futuras predicciones
        pickle.dump(regressor, open(os.path.join(fixModelPath,self.modelFile), 'wb'))
        with open(os.path.join(fixModelPath,descFile), 'w+') as f:
            f.write('MAE: ' + str(metrics.mean_absolute_error(y_test, deltasPred)) + '\n')
            f.write('MSE: ' + str(metrics.mean_squared_error(y_test, deltasPred)) + '\n')
            f.write('RMSE: ' + str(np.sqrt(metrics.mean_squared_error(y_test, deltasPred))) + '\n')
            f.write('Size: ' + str(len(self.RealCompounds)))
        #coeffs = pd.DataFrame(regressor.coef_, descriptorsDataFrame.columns, columns=['Coefficient'])
        #Tambien se debe guardar los datos de la regresion en un diccionario y CREAR y escribirlos
        #al archivo values en el formato:
        #drugclass
        #x1:a
        #x2:b
        FinalScreen = Resultados.Resultados(self.cleanDeltas,self.project_path)
        self.gui.callDestroy()