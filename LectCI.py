import tkinter as tk
from tkinter.ttk import *
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
from threading import Lock

compoundsMissed = []
length_compounds = 0
length_proteins = 0
valuecompounds = 0
valueproteins = 0
lockCompounds = Lock()
lockProteins = Lock()

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
                    #messagebox.showerror(title="ERROR", message="Formato Equivocado")
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
    connect_DrugBankBA(compounds,project_path)
    connectPubChem(compounds,project_path)

################################################################
########################Funcion de conexion a DrugBank estructura compuesto###################

def setCompoundsValue(value):
    global length_compounds
    length_compounds = value
    print("Valor compuestos: " + str(length_compounds))

def setProteinsValue(value):
    global length_proteins
    length_proteins = value
    print("Valor proteinas: " + str(length_proteins))
