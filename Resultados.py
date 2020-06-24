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
    import sys
    
except:
    import tkinter as tk
    import tkinter.font as tkFont
    from tkinter import ttk
    from PIL import ImageTk, Image
    import operator
    import numpy as np
    from tkinter import messagebox
    import os
    import sys

class Resultados():
    def __init__(self,Efectividad,Full_Path):
        ## ----- Declaración de variables ----- #
        self.y=[]
        self.y_1=[]
        self.x=[]
        self.x_1=[]
        self.i=0
        self.j=0
        self.a=0
        self.Efectividad = Efectividad
        self.Full_Path = Full_Path
        self.check_guardado = 0

        current_path = os.path.dirname(__file__)
        rel_path="Logotipo/"
        abs_file_path=os.path.join(current_path,rel_path)
        
        ## ------ Ordenamos el diccionario ------- ##
        Efectividad_Ord = sorted(Efectividad.items(), key=operator.itemgetter(1))
        for name in enumerate(Efectividad_Ord):
            print(name[1][0], Efectividad[name[1][0]])
            self.y.append(name[1][0])
            self.x.append(Efectividad[name[1][0]])
            self.i= self.i+1
        print("\n\nNumero de compuestos",self.i)

        ## --------- Quitamos c0 de los compuestos
        for name in self.y:
            self.y_1.append(name.replace('c0',''))
        print(self.y_1)
        ## ------- Ponemos Kcal/mol en efectividad ------- ##
        for name in self.x:
            self.x_1.append(str(name) + ' Kcal/mol')
            
        print(self.x_1)

        ## --------------------- Configuracion de la ventana ------------------------- ##    
        self.app = tk.Toplevel()
        self.app.title("SisPAF")
        self.app.geometry('800x500-250-150')	#Largo- Ancho| Izquierda Arriba
        self.app.configure(bg='white')

        ## ----- Labels ------- ##
        self.Titulo = tk.Label(self.app , text="Sistema para la Predicción",bg="White")
        self.Titulo.place(x=65,y=50)
        self.Titulo.config(font=("Arial",18))

        self.Titulo2 = tk.Label(self.app , text="de Actividad Farmacológica",bg="White")
        self.Titulo2.place(x=352,y=50)
        self.Titulo2.config(font=("Arial",18))

        ## ---- Logotipo ----- ##
        imagenAnchuraMaxima=150
        imagenAlturaMaxima=150
        
        # abrimos una imagen
        current_log="Logotipo2.png"
        img=Image.open(abs_file_path+current_log)
        
        # modificamos el tamaño de la imagen
        img.thumbnail((imagenAnchuraMaxima,imagenAlturaMaxima), Image.ANTIALIAS)
        
        # Convertimos la imagen a un objeto PhotoImage de Tkinter
        tkimage = ImageTk.PhotoImage(img)
        
        # Ponemos la imagen en un Lable dentro de la ventana
        label=tk.Label(self.app, image=tkimage, width=imagenAnchuraMaxima, height=imagenAlturaMaxima,bg='white').place(x=610 , y=130)
        
        '''
        #Boton de ayuda
        current_help="Imagenes/ayuda.png"
        help_=tk.PhotoImage(current_path+current_help)
        help_ima=help_.subsample(30,30)
        h_button=tk.Button(self.app,image=help_ima,text="Ayuda",font=("Arial Black",20), bg="white", relief='flat', compound="left" )
        h_button.place(x=50,y=410, in_= self.app)
        ''' 
        
        ## ------ Botones ------- ##
          # Boton Salir
        self.Boton_S = tk.Button(self.app, text="Salir", command = self.Salir)
        #self.Boton_I = tk.Button(self.app, text="Inicio", command = self.Inicio)
        self.Boton_G = tk.Button(self.app, text="Guardar", command = self.Guardar)

        ## ---------------- Tabla ----------------- ##


        self.style = ttk.Style(self.app)
        self.style.configure('Treeview',rowheight=27)
        self.app.treeview = ttk.Treeview(self.app,columns=("Efectividad"))
        self.app.treeview.heading("#0", text="Compuesto")   
        self.app.treeview.heading("Efectividad", text="Efectividad")
        self.app.treeview.place(x=105,y=100)
        self.app.treeview.column('#0')
        self.app.treeview.column("#0", width=290, anchor="n")
        self.app.treeview.column("Efectividad", width=135, anchor="n")

                ## Scroll
        vsb = ttk.Scrollbar(self.app, orient="vertical", command=self.app.treeview.yview)
        vsb.place(x=485+22, y=100, height=292)
        self.app.treeview.configure(yscrollcommand=vsb.set)

                #Llenado de tabla
        for var in self.x_1:
            self.app.treeview.insert("",tk.END, text=self.y_1[self.j],values=self.x_1[self.j])
            self.j = self.j+1
        self.ver()    
    
        ## ------ Funciones ------ ##
    def Salir(self):
        if self.check_guardado == 0:
            mensaje = messagebox.askyesno('Advertencia','No se han guardado sus resultados\n¿Desea continuar?',parent=self.app)
            if mensaje == True:
                sys.exit(0)
            else:
                print("Nada")
        else:
            sys.exit(0)
    '''
    def Inicio(self):
        if self.check_guardado == 0:
            mensaje = messagebox.askyesno('Advertencia','No se han guardado sus resultados\n¿Desea continuar?')
            if mensaje == True:
                self.app.destroy()
                #First = Principal.Principal()
            else:
                print("Nada")
        else:
            self.app.destroy()
            #First = Principal.Principal()
    '''
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

        if os.path.isfile(full_path):
            print("Archivo existe")
        else:
            archivo = open(full_path,"w")
            archivo.write("----------------------------- Resultados ----------------------------|\n\n")
            archivo.write("------------ Compounds ------------ | --------- Efectividad ---------|\n")

            for var in self.x_1:
                archivo.write(self.y_1[i])
                tam = (Com_tam - len(self.y_1[i]))

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
            
        messagebox.showinfo("Resultados Guardados","Guardado correctamente",parent=self.app)
        self.check_guardado = 1

    def ver (self):
        #self.Boton_I.place(x=690, y=360)
        self.Boton_G.place(x=685, y=360)
        self.Boton_S.place(x=610, y=360)
        self.app.protocol("WM_DELETE_WINDOW", self.Salir)

