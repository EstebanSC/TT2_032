import tkinter as tk
import CenterScreen
import os
from PIL import Image, ImageTk  

class CustomSpanishDialog():
    def __init__(self):
        self.base = tk.Toplevel()
        self.retValue = False
        current_path = os.path.dirname(__file__) # Where your .py file is located
        self.base.title("Alerta")
        self.label = tk.Label(self.base, text="En este directorio ya existe un proyecto. \nCrear uno nuevo sobreescribirá el proyecto existente. \n¿Desea continuar?")
        self.label.grid(row=0, column=1, columnspan=3)
        rel_path2="Interfaces/"
        abs_file_path2=os.path.join(current_path,rel_path2)
        current_log="Warning.png"
        self.photo_log=tk.PhotoImage(file=abs_file_path2+current_log)
        self.pp=self.photo_log.subsample(18,18)
        self.LogoP=tk.Label(self.base,height=150, width=150, image=self.pp)
        self.LogoP.grid(row=0,column=0, columnspan=3)
        self.button1 = tk.Button(self.base, text="SI", command=self.ok)
        #self.button1.pack()
        self.button1.grid(row=1, column=0)
        self.button2 = tk.Button(self.base, text="NO", command=self.okno)
        #self.button2.pack()
        self.button2.grid(row=1, column=2)
        CenterScreen.center_screen(self.base)

    def ok(self):
        self.retValue = True
        self.base.destroy()

    def okno(self):
        self.base.destroy()
    
    def getValue(self):
        return self.retValue