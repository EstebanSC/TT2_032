import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import os


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
######################################################################3
########################Funcion de conexion a DrugBank estructura compuesto###################
def connect_DrugBank(compounds):
    #Driver using mozzila to acces a drugbank
    opt=webdriver.ChromeOptions()
    opt.add_argument('headless')
    driveC= webdriver.Chrome(chrome_options=opt)
    #driveC=webdriver.PhantomJS()
    current_path = os.path.dirname(__file__)
    for x in range(len(compounds)):
        ruta=current_path+"/Compounds/"+compounds[x]+".txt"##Creacion del archivo, String de la ruta
        driveC.get('https://www.drugbank.ca/')
        inputNCom=driveC.find_element_by_id('query')#Explication to manager websites 
                                                        #actions in https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08
        inputNCom.send_keys(compounds[x])
        inputNCom.send_keys(Keys.ENTER)
        struct_Down=driveC.find_element_by_xpath('//*[@id="structure-download"]/div/a[4]').get_attribute('href')#Se consigue
        r=requests.get(str(struct_Down))
        filet=open(ruta,"tw")
        filet.write(r.text)
        ##el elemnto html tipo <a> y adquirimos la direccion url
    ##uct_Down.click()
        #direct= driveC.current_url
        #print(struct_Down)
        
    print('Check')
    driveC.close()
########################################################################################
                

