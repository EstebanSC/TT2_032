try:
    import Tkinter as tk
    import tkinter.font as tkFont
    from tkinter import ttk
    from PIL import ImageTk, Image
    import operator
    import numpy as np
    from tkinter import messagebox
    from Tkinter import * 
    
except:
    import tkinter as tk
    import tkinter.font as tkFont
    from tkinter import ttk
    from PIL import ImageTk, Image
    import operator
    import numpy as np
    from tkinter import messagebox

class Resultados(self):
    ## ----- Declaración de variables ----- #
    y=[]
    x=[]
    i=0
    j=0
    a=0
    Efectividad = {}
    '''
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
    '''
    ## ------ Ordenamos el diccionario ------- ##
    Efectividad_Ord = sorted(Efectividad.items(), key=operator.itemgetter(1), reverse=True)
    for name in enumerate(Efectividad_Ord):
        print(name[1][0], Efectividad[name[1][0]])
        y.append(name[1][0])
        x.append(Efectividad[name[1][0]])
        i= i+1
    print("\n\nNumero de compuestos",i)

    ## --------------------- Configuracion de la ventana ------------------------- ##    
    app = tk.Tk()
    app.title("SysPAF - Resultados")
    app.geometry("800x500-250-150")	#Largo- Ancho| Izquierda Arriba
    app.configure(bg='white')

    ## ----- Labels ------- ##
    Titulo = tk.Label(app , text="Sistema para la Predicción",bg="White")
    Titulo.place(x=65,y=50)
    Titulo.config(font=("Arial",18))

    Titulo2 = tk.Label(app , text="de Actividad Farmacologica",bg="White")
    Titulo2.place(x=352,y=50)
    Titulo2.config(font=("Arial",18))

    ## ---- Logotipo ----- ##
    imagenAnchuraMaxima=150
    imagenAlturaMaxima=150
    
    # abrimos una imagen
    img = Image.open('Imagenes/Logotipo2.png')
    
    # modificamos el tamaño de la imagen
    img.thumbnail((imagenAnchuraMaxima,imagenAlturaMaxima), Image.ANTIALIAS)
    
    # titulo de la ventana
    app.title("Mostrar imagen")
    
    # Convertimos la imagen a un objeto PhotoImage de Tkinter
    tkimage = ImageTk.PhotoImage(img)
    
    # Ponemos la imagen en un Lable dentro de la ventana
    label=tk.Label(app, image=tkimage, width=imagenAnchuraMaxima, height=imagenAlturaMaxima,bg='white').place(x=610 , y=130)

    #Boton de ayuda
    current_help="Imagenes/ayuda.png"
    help_=tk.PhotoImage(file=current_help)
    help_ima=help_.subsample(30,30)
    h_button=tk.Button(app,image=help_ima,text="Ayuda",font=("Arial Black",20), bg="white", relief='flat', compound="left" )
    h_button.place(x=50,y=410, in_=app)


    ## ------ Funciones ------ ##
    def Salir():
        app.destroy()

    #def Inicio():
    #   app

    def Guardar():
        i=0
        Com_tam = 36
        Efe_tam = 13
        relleno = 32

        archivo = open("Resultados/Resultados_Proyecto.txt","w")
        archivo.write("----------------------------- Resultados ----------------------------|\n\n")
        archivo.write("------------ Compounds ------------ | --------- Efectividad ---------|\n")

        for var in x:
            archivo.write(y[i])
            tam = (Com_tam - len(y[i]))

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
        

    ## ------ Botones ------- ##
        # Boton Salir
    B_Salir = tk.Button(app, text="Salir", command=Salir)
    B_Salir.place(x=620, y=360)

    B_Nuevo = tk.Button(app, text="Inicio")
    B_Nuevo.place(x=690, y=360)

    B_Nuevo = tk.Button(app, text="Guardar", command=Guardar)
    B_Nuevo.place(x=645, y=320)


    ## ---------------- Tabla ----------------- ##

    style = ttk.Style(app)
    style.configure('Treeview',rowheight=27)
    app.treeview = ttk.Treeview(app,columns=("Score"))
    app.treeview.heading("#0", text="Compuesto")   
    app.treeview.heading("Score", text="Score")
    app.treeview.place(x=85,y=100)
    app.treeview.column('#0',stretch=True)
    app.treeview.column("#0", width=390, anchor="center")
    app.treeview.column("Score", width=100, anchor="center")

            ## Scroll
    vsb = ttk.Scrollbar(app, orient="vertical", command=app.treeview.yview)
    vsb.place(x=575, y=100, height=292)
    app.treeview.configure(yscrollcommand=vsb.set)

            #Llenado de tabla
    for var in x:
        app.treeview.insert("",tk.END, text=y[j],values=x[j])
        j = j+1

    app.mainloop()



