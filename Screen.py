import tkinter as tk
from tkinter.ttk import*
from tkinter import *
from tkinter import  filedialog, Text
from PIL import Image, ImageTk 
from LectCI import *
import threading
import os 
import time
### Definicion de la pantalla descargas, implementar GIF'S
class WaitSearchData():
    compounds=[] #Arreglos globales de compuestos
    proteins=[]#Arreglos proteinasn
    project_path=""#Directorio del proyecto

    def __init__(self):
        current_path = os.path.dirname(__file__) # Where your .py file is located
        self.pantalla=tk.Toplevel()
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
        #rel_path="Interfaces/"
        #abs_file_path=os.path.join(current_path,rel_path)
        #current_file="giphy.gif"
        #self.photo=PhotoImage(file=abs_file_path+current_file, format="gif -index 2")
        #self.photo_bu=self.photo.subsample(1,1)
        #self.charge=Label(self.pantalla,height=400, width=400, image=self.photo_bu,bg="white")
        self.charge=Progressbar(self.pantalla,mode="indeterminate",maximum=25)
        #self.charge.pack()
        

    def showScreen(self):
        self.pantalla.title("Busqueda")
        self.pantalla.geometry("850x450")
        self.center_screen()
        self.header.place(x=25,y=50)
        self.charge.place(x=250,y=250, width=350)
        self.charge.start()
        time.sleep(3)
       
    def ask_quit(self):
        if messagebox.askokcancel("Cerrar", "Desea cerrar la busqueda de datos ?",parent=self.pantalla):
            self.pantalla.destroy()
    
    def center_screen(self):
       self.pantalla.update_idletasks()
       width = self.pantalla.winfo_reqwidth()
       height = self.pantalla.winfo_reqheight()
       x = (self.pantalla.winfo_screenwidth() // 2) - (width // 2)
       y = (self.pantalla.winfo_screenheight() // 2) - (height // 2)
       self.pantalla.geometry('{}x{}+{}+{}'.format(width, height, x, y))
       #self.pantalla.geometry("%dx%d+%d+%d" % (850, 450, x_coord, y_coord))

    #NOTA: ESTA FUNCION NO SE ESTA UTILIZANDO 25-Abril-2020
    def  procesos(self,compounds,proteins,project_path):
        compound_threads = list()
        protein_threads = list()

        #show_s=threading.Thread(target=self.showScreen)
        #time.sleep(0.1)
        
        #crear hilos para compuestos
        for item in compounds:  #Un hilo por cada elemento del arreglo compounds
            get_compound = threading.Thread(target=alldata_compunds,args=(item, project_path)) #creacion del hilo, argumentos: un solo compuesto y path
            compound_threads.append(get_compound)   #agregar hilo a la lista de hilos de compuestos 
            get_compound.start()    #comenzar hilos
        
        #crear hilos para proteinas (proceso equivalente al de compuestos, pero ahora se usan los items del arreglo proteins)
        for item in proteins:
            get_protein = threading.Thread(target=connect_PDB,args=(item, project_path))
            protein_threads.append(get_protein)  
            get_protein.start()

        """for index,item in enumerate(compound_threads):  #bucle (ordenado e indexado) para esperar a que los hilos terminen su ejecucion
            item.join()
            print('hilo COMPUESTO numero:',index, 'FINALIZADO')
        
        for index,item in enumerate(protein_threads):
            item.join()
            print('hilo PROTEINA numero:',index, 'FINALIZADO')"""

        #show_s.start()
    
        print("acabo funcion")
        #NOTA: EL CAMBIO EN LOS LABELS ES SOLO DE PRUEBA VISUAL, NO DETERMINA LO QUE EL PROGRAMA SE ENCUENTRA
        #SE ENCUENTRA HACIENDO EN ESE MOMENTO
        self.search_end()
        self.show_results()

    #NOTA: ESTO ES UNA FUNCION PARA PRUEBAS VISUALES
    def search_end(self):
        self.change_title("Finalizando busqueda...",2)
        self.change_title("Recopilando resultados...",3)
        
    
    def change_title(self,text,duration):
        self.r=text
        time.sleep(duration)
        self.title.set(self.r)
        self.header.config(text=self.title)
    
    def destroy_screen(self):
        self.pantalla.destroy()
    
    def show_results(self):
        self.change_title("RESULTADOS DE LA BUSQUEDA",1)
        self.charge.destroy()
        