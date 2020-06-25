
def center_screen(current_screen):    #Funcion para centrar la pantalla
       current_screen.update_idletasks()
       width = current_screen.winfo_width()
       height = current_screen.winfo_height()
       x = (current_screen.winfo_screenwidth() // 2) - (width // 2)
       y = (current_screen.winfo_screenheight() // 2) - (height // 2)
       current_screen.geometry('{}x{}+{}+{}'.format(width, height, x, y))