try:
    import Tkinter as tk
    import tkinter.font as tkFont
    from tkinter import ttk
    from PIL import ImageTk, Image
    import operator
    import numpy as np
    from tkinter import messagebox
    from Tkinter import * 
    import os
    
except:
    import tkinter as tk
    import tkinter.font as tkFont
    from tkinter import ttk
    from PIL import ImageTk, Image
    import operator
    import numpy as np
    from tkinter import messagebox
    import os

class Resultados():
    def __init__(self,Efectividad,Full_Path):
        ## ----- Declaración de variables ----- #
        self.y=[]
        self.x=[]
        self.i=0
        self.j=0
        self.a=0
        self.Efectividad = Efectividad
        self.Full_Path = Full_Path
        
        ## ------ Ordenamos el diccionario ------- ##
        Efectividad_Ord = sorted(Efectividad.items(), key=operator.itemgetter(1), reverse=True)
        for name in enumerate(Efectividad_Ord):
            print(name[1][0], Efectividad[name[1][0]])
            self.y.append(name[1][0])
            self.x.append(Efectividad[name[1][0]])
            self.i= self.i+1
        print("\n\nNumero de compuestos",self.i)

        ## --------------------- Configuracion de la ventana ------------------------- ##    
        self.app = tk.Tk()
        self.app.title("SysPAF - Resultados")
        self.app.geometry("800x500-250-150")	#Largo- Ancho| Izquierda Arriba
        self.app.configure(bg='white')

        ## ----- Labels ------- ##
        self.Titulo = tk.Label(self.app , text="Sistema para la Predicción",bg="White")
        self.Titulo.place(x=65,y=50)
        self.Titulo.config(font=("Arial",18))

        self.Titulo2 = tk.Label(self.app , text="de Actividad Farmacologica",bg="White")
        self.Titulo2.place(x=352,y=50)
        self.Titulo2.config(font=("Arial",18))

        ## ---- Logotipo ----- ##
        imagenAnchuraMaxima=150
        imagenAlturaMaxima=150
        
        # abrimos una imagen
        img = Image.open('Imagenes/Logotipo2.png')
        
        # modificamos el tamaño de la imagen
        img.thumbnail((imagenAnchuraMaxima,imagenAlturaMaxima), Image.ANTIALIAS)
        
        # Convertimos la imagen a un objeto PhotoImage de Tkinter
        tkimage = ImageTk.PhotoImage(img)
        
        # Ponemos la imagen en un Lable dentro de la ventana
        label=tk.Label(self.app, image=tkimage, width=imagenAnchuraMaxima, height=imagenAlturaMaxima,bg='white').place(x=610 , y=130)

        #Boton de ayuda
        current_help="Imagenes/ayuda.png"
        help_=tk.PhotoImage(file = current_help)
        help_ima=help_.subsample(30,30)
        h_button=tk.Button(self.app,image=help_ima,text="Ayuda",font=("Arial Black",20), bg="white", relief='flat', compound="left" )
        h_button.place(x=50,y=410, in_= self.app)        

        ## ------ Botones ------- ##
          # Boton Salir
        self.Boton_S = tk.Button(self.app, text="Salir", command = self.Salir)
        self.Boton_I = tk.Button(self.app, text="Inicio")
        self.Boton_G = tk.Button(self.app, text="Guardar", command = self.Guardar)

        ## ---------------- Tabla ----------------- ##

        self.style = ttk.Style(self.app)
        self.style.configure('Treeview',rowheight=27)
        self.app.treeview = ttk.Treeview(self.app,columns=("Score"))
        self.app.treeview.heading("#0", text="Compuesto")   
        self.app.treeview.heading("Score", text="Score")
        self.app.treeview.place(x=85,y=100)
        self.app.treeview.column('#0',stretch=True)
        self.app.treeview.column("#0", width=390, anchor="center")
        self.app.treeview.column("Score", width=100, anchor="center")

                ## Scroll
        vsb = ttk.Scrollbar(self.app, orient="vertical", command=self.app.treeview.yview)
        vsb.place(x=575, y=100, height=292)
        self.app.treeview.configure(yscrollcommand=vsb.set)

                #Llenado de tabla
        for var in self.x:
            self.app.treeview.insert("",tk.END, text=self.y[self.j],values=self.x[self.j])
            self.j = self.j+1
        self.ver()    
    
        ## ------ Funciones ------ ##
    def Salir(self):
        self.app.destroy()

    #def Inicio():
    #   app

    def Guardar(self):
        i=0
        Com_tam = 36
        Efe_tam = 13
        relleno = 32
        full_path = self.Full_Path + '/Resultados/Resultados_Proyecto.txt'
        check = self.Full_Path + '/Resultados'
        print(check)
        if os.path.isdir(check):
            print('directorio exites')
        else:
            print('Creando carpeta')
            os.chdir(self.Full_Path)
            os.mkdir('Resultados')
        

        archivo = open(full_path,"w")
        archivo.write("----------------------------- Resultados ----------------------------|\n\n")
        archivo.write("------------ Compounds ------------ | --------- Efectividad ---------|\n")

        for var in self.x:
            archivo.write(self.y[i])
            tam = (Com_tam - len(self.y[i]))

            for espacio in range(tam):
                archivo.write(" ")
            archivo.write("|")

            for espacio in range(Efe_tam):
                archivo.write(" ")
            archivo.write(str(var))
            tam_1 = (relleno-len(str(var))-Efe_tam)

            for espacio in range(tam_1):
                archivo.write(" ")
            archivo.write("|")
            archivo.write("\n")
            i=i+1
        for target_list in range(70):
            archivo.write("-")
        
        messagebox.showinfo("Resultados Guardados","Guardado correctamente")

    def ver (self):
        self.Boton_I.place(x=690, y=360)
        self.Boton_G.place(x=645, y=320)
        self.Boton_S.place(x=620, y=360)
        self.app.mainloop()

## ------ Declaramos un diccionario como prueba ---- ##
Efectividad = {
'Salbutamoll': 1.99,
'Beclomethasone_dipropionatee': 10.300,
'Alprenololl': 30.61,
'Lidocainee': 45.35,
'Paracetamoll': 11.1,
'Omeprazolee': 60.45,
'Salbutamol': 55.46,
'Beclomethasone_dipropionate': 18,
'Alprenolol': 80.12,
'Lidocaine': 70.15,
'Lidocaineeñ': 50.35,
'Paracetamollñ': 20.1,
'Omeprazoleeñ': 25.45,
'Salbutamole': 35.46,
'Beclomethasone_dipropionatele': 60,
'Alprenolole': 32.2,
'Lidocaineie': 11.15
}

full_path = '/home/erikmc10/Documentos/RL'

Resultados = Resultados(Efectividad,full_path)