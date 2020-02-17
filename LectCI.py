import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import messagebox
import os

#Implementacion de lecturas

def lectura(filenom):
    conjuntoinicial=open(filenom,"tr")#Se abre el archivo, t se especifica que es un txt, r =read
    lines=list(conjuntoinicial.readlines())
    #print(lines[0])
    flagtype=0
    compounds=[]
    proteins=[]
    #print(lines)
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
                return
            elif(flagtype==1):
                compounds.append(strline)
                continue
            elif(flagtype==2):
                proteins.append(strline)
                continue
    #print(compounds)
    #print(proteins)
    return [compounds, proteins]


                

