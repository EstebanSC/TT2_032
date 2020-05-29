from tkinter import ttk
import tkinter as tk
from tkinter import PhotoImage
import os

current_path = os.path.dirname(__file__)
win = tk.Tk()
win.minsize(width=600, height=400)
win.resizable(width=0, height=0)

rel_path2="Interfaces/"
abs_file_path=os.path.join(current_path,rel_path2)

current_logS="Success.png"
current_logE="Error.png"
current_logW="Warning.png"
imgSS = PhotoImage(file=abs_file_path+current_logS)
imgEE= PhotoImage(file=abs_file_path+current_logE)
imgWW=PhotoImage(file=abs_file_path+current_logW)
imgS=imgSS.subsample(5,5)

tree = ttk.Treeview(win, selectmode='browse')
tree.place(x=30, y=95)

treeP=ttk.Treeview(win, selectmode='browse')
treeP.place(x=330,y=95)

vsbP=ttk.Scrollbar(win, orient="vertical", command=treeP.yview)
vsbP.place(x=330+200+2, y=95, height=200+20)

treeP.configure(yscrollcommand=vsbP.set)

vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
vsb.place(x=30+200+2, y=95, height=200+20)

tree.configure(yscrollcommand=vsb.set)

tree["columns"] = ("1", "2")
tree['show'] = 'headings'
tree.column("1", width=100, anchor='c')
#tree.column("2", width=100, anchor='c')
tree.heading("#1", text="Compuestos")
tree.heading("#2", text="Resultados")

tree.insert('', 'end', text="#1's text",image= imgW,values=("Big1"))
tree.insert('', 'end', text="#1's text",image= imgW,values=("Big2"))
tree.insert('', 'end', text="#1's text",image= imgS,values=("Big3"))
tree.insert('', 'end', text="#1's text",image= imgE,values=("Big4"))
tree.insert('', 'end', text="#1's text",image= imgW,values=("Big5"))
tree.insert('', 'end', text="#1's text",image= imgS,values=("Big6"))
tree.insert('', 'end', text="#1's text",image= imgS,values=("Big7"))
tree.insert('', 'end', text="#1's text",image= imgS,values=("Big8"))
tree.insert('', 'end', text="#1's text",image= imgE,values=("Big9"))
tree.insert('', 'end', text="#1's text",image= imgW,values=("Big10"))
tree.insert('', 'end', text="#1's text",image= imgS,values=("Big11"))
tree.insert('', 'end', text="#1's text",image= imgW,values=("Big12"))

treeP["columns"] = ("1", "2")
treeP['show'] = 'headings'
treeP.column("1", width=100, anchor='c')
treeP.column("2", width=100, anchor='c')
treeP.heading("1", text="Account")
treeP.heading("2", text="Type")
treeP.insert("",'end',text="L1",values=("Big1","Best"))
treeP.insert("",'end',text="L2",values=("Big2","Best"))
treeP.insert("",'end',text="L3",values=("Big3","Best"))
treeP.insert("",'end',text="L4",values=("Big4","Best"))
treeP.insert("",'end',text="L5",values=("Big5","Best"))
treeP.insert("",'end',text="L6",values=("Big6","Best"))
treeP.insert("",'end',text="L7",values=("Big7","Best"))
treeP.insert("",'end',text="L8",values=("Big8","Best"))
treeP.insert("",'end',text="L9",values=("Big9","Best"))
treeP.insert("",'end',text="L10",values=("Big10","Best"))
treeP.insert("",'end',text="L11",values=("Big11","Best"))
treeP.insert("",'end',text="L12",values=("Big12","Best"))


win.mainloop()

