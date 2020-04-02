import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import messagebox
#from bs4 import BeautifulSoup
from selenium import webdriver
from Bio.PDB import *
from selenium.webdriver.common.keys import Keys
import requests
import os
import time
import pubchempy as pcp
import json
import threading



#Implementacion de lecturas del archivo que contiene nombre de compuestos y proteinas
def lectura(filenom):
    conjuntoinicial=open(filenom,"tr")#Se abre el archivo, t se especifica que es un txt, r =read
    lines=list(conjuntoinicial.readlines())
    #print(lines[0])
    flagtype=0
    compounds=[]
    proteins=[]
    #print(lines)
    try:
        for line in lines:
        #print(line)
            strline=str(line)  
            strline=strline.replace('\n','') 
            if(strline=="Compounds"):##La linea que indique el inicio de compuestos
                flagtype=1
                continue
            elif(strline=="Proteins") :#La linea que indique el inicio de proteinas
                flagtype=2
                continue
            else:
                if(flagtype==0):
                    messagebox.showerror(title="ERROR", message="Formato Equivocado")
                    return[compounds,proteins]
                elif(flagtype==1):
                    compounds.append(strline)
                    continue
                elif(flagtype==2):
                    proteins.append(strline)
                    continue
    
        return [compounds, proteins]
    except:
        messagebox.showerror(title="ERROR", message="Formato Equivocado")
        return[compounds,proteins]
######################################################################
################Funcion Conseguir Datos de Compuestos############
def alldata_compunds(compounds,project_path):
    connect_DrugBank(compounds,project_path)
    connectPubChem(compounds,project_path)
    connect_DrugBankBA(compounds,project_path)
################################################################
########################Funcion de conexion a DrugBank estructura compuesto###################
def connect_DrugBank(compounds, project_path):
    #Driver using mozzila to acces a drugbank
    opt=webdriver.ChromeOptions()
    opt.add_argument('headless')
    driveC= webdriver.Chrome(chrome_options=opt)
    #driveC=webdriver.PhantomJS()
    print(compounds)
    print(project_path)
    current_path = os.path.dirname(__file__)
    
    for x in range(len(compounds)):
        #llamar funcion
        #generararchivo(pathdeaquiabajo, 2)
        #ruta=current_path+"/Compounds/"+compounds[x]+".txt"##Creacion del archivo, String de la ruta
        ruta=project_path+"/Compounds/c0"+compounds[x]+".txt"##Creacion del archivo, String de la ruta
        driveC.get('https://www.drugbank.ca/')
        inputNCom=driveC.find_element_by_id('query')#Explication to manager websites 
                                                        #actions in https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08
        inputNCom.send_keys(compounds[x])
        inputNCom.send_keys(Keys.ENTER)
        struct_Down=driveC.find_element_by_xpath('//*[@id="structure-download"]/div/a[4]').get_attribute('href')#Se consigue
        r=requests.get(str(struct_Down))
        filet=open(ruta,"tw")
        filet.write("STRUCTURE:\n")
        filet.write(r.text)
        filet.write("##########\n")
        
        ##el elemnto html tipo <a> y adquirimos la direccion url
    ##uct_Down.click()
        #direct= driveC.current_url
        #print(struct_Down)
    driveC.close()
    #call pubChem
    #dataPubChem = threading.Thread(target=connectPubChem, args=(compounds,project_path))
    #dataPubChem.start()
    print('Check')
########################################################################################
#############################Conexion a DrugBank BA###########################################
def connect_DrugBankBA(compounds, project_path):
    #Driver using mozzila to acces a drugbank
    #x=0
    opt=webdriver.ChromeOptions()
    opt.add_argument('headless')
    driveC= webdriver.Chrome(chrome_options=opt)
    for x in range(len(compounds)):
        ruta=project_path+"/Compounds/c0"+compounds[x]+".txt"##Creacion del archivo, String de la ruta
        driveC.get('https://www.drugbank.ca/')
        inputNCom=driveC.find_element_by_id('query')#Explication to manager websites 
                                                    #actions in https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08
        inputNCom.send_keys(compounds[x])
        inputNCom.send_keys(Keys.ENTER)
        try:
            driveC.implicitly_wait(5)
            #tableBA=driveC.find_element_by_tag_name("table")
            #files=tableBA.find_elements_by_tag_name("tr")
            #tbdy=driveC.find_element_by_xpath('//*[@id="drug-moa-target-table"]')
            #table=driveC.find_element_by_id("drug-moa-target-table")
            tds=driveC.find_element_by_xpath('//*[@id="drug-moa-target-table"]/tbody')
            arr=tds.find_elements_by_tag_name("td")
            array_p=""
            filet=open(ruta,"ta")
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
            print("Table founded:"+str(x))
            filet.write("##########\n")
            #print(table)
        except:
            filet=open(ruta,"ta")
            filet.write("BIOACTIVITY:\n")
            filet.write("EMPTY:NOT FOUND\n")
            filet.write("##########\n")
            print("Table not founded:"+str(x))
    print("fni")  
########################################################################################
#############################Conexion a PDB###########################################
def connect_PDB(proteins,project_path):
    current_path = os.path.dirname(__file__)
    opt=webdriver.ChromeOptions()
    opt.add_argument('headless')
    #driveC= webdriver.Chrome(chrome_options=opt)
    for x in range(len(proteins)):
        driveC= webdriver.Chrome(chrome_options=opt)
        #ruta=current_path+"/Proteins/"+proteins[x]+".txt"
        ruta=project_path+"/Proteins/p0"+proteins[x]+".txt"##Creacion del archivo, String de la ruta
        driveC.get('https://www.rcsb.org/')
        inputPro=driveC.find_element_by_id('autosearch_SearchBar')#Explication to manager websites 
        inputPro.send_keys(proteins[x])
        clickS=driveC.find_element_by_id('searchbutton')#
        clickS.click()
        driveC.implicitly_wait(5)
        ids=driveC.find_element_by_tag_name("h3")
        #ids.reverse()
        path_dp="https://files.rcsb.org/view/"+ids.text+".pdb"
        r=requests.get(path_dp)
        filet=open(ruta,"tw")
        filet.write(r.text)
        driveC.delete_all_cookies()
        
    #dirc=ids[0].find_elements_by_tag_name("a")
    #print(dirc[0].get_attribute("href"))
    #print(ids[0].text)
    #pdbl = PDBList()
    #pdbl.retrieve_pdb_file('1FAT',pdir=ruta)
    #print(getid)
    driveC.close()
    print("Finish")

#Funcion para obtener datos de Pubchem
def connectPubChem(compounds, project_path):
    #Looking for each compound
    time.sleep(10)
    recovery_pointer = 0        #Usar esto para cuando se pierda el progreso de obtencion de informacion
    compoundsFounded = []
    compoundsMissed = []
    new_dict = {}
    #f = open("prueba.txt", "a+")
    #Computed properties available in PubChem
    computedProperties = ['MolecularWeight', 'XLogP', 'HBondDonorCount', 'HBondAcceptorCount',
                        'RotatableBondCount', 'ExactMass', 'MonoisotopicMass', 
                        'TPSA', 'HeavyAtomCount', 'Charge', 'Complexity', 'IsotopeAtomCount', 
                        'DefinedAtomStereoCount', 'UndefinedAtomStereoCount', 'DefinedBondStereoCount', 
                        'UndefinedBondStereoCount', 'CovalentUnitCount']

    for item in compounds:
        c = pcp.get_compounds(item, 'name')
        if c == []:
            compoundsMissed.append(item)
        else:
            compoundsFounded.append(item)
        #print(c)


    #for each compound founded, try to retrieve its properties
    #Computed properties
    for item in compoundsFounded:
        ruta = project_path + "/Compounds/c0" + item +".txt"
        p = pcp.get_properties(computedProperties, item, 'name')
        for i in p:
            del i['CID']
            with open(ruta, 'a+') as file:
                file.write("DESCRIPTORS:\n")
                json.dump(i, file, sort_keys=True, indent = 2)
                file.write("\n##########\n")
        #print(p)
        #Write to its "zero set" file (APPEND)

    file.close()
    print("Finish: retrieved all descriptors")

