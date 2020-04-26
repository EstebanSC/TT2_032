import threading
import time 
from Screen import *
from LectCI import *


####################En esta funcion se mandan a llamar las funciones donde se obtiene info de cada DB
def get_data(compounds, proteins,project_path):
    #Instanciando clase WaitSearchData
    w=WaitSearchData()
    #Crear hilo para pantalla
    showScreen=threading.Thread(target=w.showScreen)
    showScreen.start()
    #Crear hilo procesos
    compound_threads = list()
    protein_threads = list()
        
    #crear hilos para compuestos
    for item in compounds:  #Un hilo por cada elemento del arreglo compounds
        #print(item)
        get_compound = threading.Thread(target=alldata_compunds,args=(item, project_path)) #creacion del hilo, argumentos: un solo compuesto y path
        compound_threads.append(get_compound)   #agregar hilo a la lista de hilos de compuestos 
        get_compound.start()    #comenzar hilos
        
        #crear hilos para proteinas (proceso equivalente al de compuestos, pero ahora se usan los items del arreglo proteins)
    for item in proteins:
        #print("PROTEINA ENVIADA: " + item)
        get_protein = threading.Thread(target=connect_PDB,args=(item, project_path))
        protein_threads.append(get_protein)  
        get_protein.start()

    """for index,item in enumerate(compound_threads):  #bucle (ordenado e indexado) para esperar a que los hilos terminen su ejecucion
        item.join()
        print('hilo COMPUESTO numero:',index, 'FINALIZADO')
        
    for index,item in enumerate(protein_threads):
        item.join()
        print('hilo PROTEINA numero:',index, 'FINALIZADO')"""
    
    print(numero)
    
##################################################