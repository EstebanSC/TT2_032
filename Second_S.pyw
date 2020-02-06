import tkinter as tk

root = tk.Tk()
root.geometry("150x150")

f1 = tk.Frame(root, background="blue")
f2 = tk.Frame(root, background="pink")

f1.pack(side="left", fill="both", expand=True)
f2.pack(side="right", fill="both", expand=True)

button = tk.Button(root, text="click me!")
button.place(x=10, y=120, in_=root)

root.mainloop()