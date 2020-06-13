from tkinter import ttk
import tkinter as tk
from tkinter import PhotoImage
import os

win = tk.Tk()
win.minsize(width=950, height=400)
win.resizable(width=0, height=0)


compounds=['Salbutamol','Beclomethasone dipropionate','Alprenolol','Lidocaine,Paracetamol','Omeprazole','Loratadine','Ramipril','Piroxicam','Diazepam','Ibuprofen','Morphine','Chlorphenamine','Aspirin','Prednisone','Epinephrine','Amoxicillin','Albendazole']
compoundsMDB1=['Salbutamol','Ramipril','Piroxicam','Diazepam']
compoundsMDB2=['Loratadine','Ramipril''Diazepam']
compoundsMissed=['Amoxicillin','Albendazole']
proteins=['Actin','Collagen','Glutaminyl','Arginine']
P_notfounds=['Actin','Collagen']
#height = 5
width = 4

current_path = os.path.dirname(__file__)
rel_path="Interfaces/"
abs_file_path=os.path.join(current_path,rel_path)
Dir_Success="correcto.png"
Dir_Error="error.png"
Dir_Warn="Advertencia.png"
imgE=PhotoImage(file=abs_file_path+Dir_Error)
imgS=PhotoImage(file=abs_file_path+Dir_Success)
imgW=PhotoImage(file=abs_file_path+Dir_Warn)

imE=imgE.subsample(70,70)
imS=imgS.subsample(100,100)
imW=imgW.subsample(100,100)

Headers=['Compuestos','Estructura','Descriptores','Bio-Actividad']
##############Container Compuestos#########
container = ttk.Frame(win)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
canvas.configure(yscrollcommand=scrollbar.set, width=570)


for i in range(len(compounds)+1): #Rows
    for j in range(width): #Columns

        if(i<1):
            b=tk.Label(scrollable_frame,text=Headers[j],fg="black",font=("Helvetica", 16))
            b.grid(row=i, column=j)
        
        else:
            if(j==0):
                lss=compounds[i-1]
                print(lss)
                b = tk.Label(scrollable_frame, text=lss)
                #print(compounds[i-1])
                b.grid(row=i, column=j)
            elif(j==1):
                if(compounds[i-1] in compoundsMDB1):
                    b = tk.Label(scrollable_frame, image=imE)
                else:
                    b = tk.Label(scrollable_frame, image=imS)
                b.grid(row=i, column=j)
            
            elif(j==2):
                if(compounds[i-1] in compoundsMissed):
                    b = tk.Label(scrollable_frame, image=imE)
                else:
                    b = tk.Label(scrollable_frame, image=imS)
                b.grid(row=i, column=j)
                
            elif(j==3):
                if(compounds[i-1] in compoundsMDB2):
                    b = tk.Label(scrollable_frame, image=imE)
                else:
                    b = tk.Label(scrollable_frame, image=imS)
                b.grid(row=i, column=j)

    
container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
container.place(x=20,y=100)
###########################################
#################Container Proteinas###########
containerP = ttk.Frame(win)
canvasP = tk.Canvas(containerP)
scrollbarP = ttk.Scrollbar(containerP, orient="vertical", command=canvasP.yview)
scrollable_frameP = ttk.Frame(canvasP)
scrollable_frameP.bind(
    "<Configure>",
    lambda e: canvasP.configure(
        scrollregion=canvasP.bbox("all")
    )
)

canvasP.create_window((0, 0), window=scrollable_frameP, anchor="n")
canvasP.configure(yscrollcommand=scrollbarP.set, width=250)

wp=2
HeadP=['Proteina','Estructura']
for i in range(len(proteins)+1): #Rows
    for j in range(wp): #Columns

        if(i<1):
            b=tk.Label(scrollable_frameP,text=HeadP[j],fg="black",font=("Helvetica", 16))
            b.grid(row=i, column=j)
        
        else:
            if(j==0):
                lss=proteins[i-1]
                print(lss)
                b = tk.Label(scrollable_frameP, text=lss)
                #print(compounds[i-1])
                b.grid(row=i, column=j)
            elif(j==1):
                if(proteins[i-1] in P_notfounds):
                    b = tk.Label(scrollable_frameP, image=imE)
                else:
                    b = tk.Label(scrollable_frameP, image=imS)
                b.grid(row=i, column=j)
            

    
containerP.pack()
canvasP.pack(side="left", fill="both", expand=True)
scrollbarP.pack(side="right", fill="y")
containerP.place(x=650,y=100)
win.mainloop()