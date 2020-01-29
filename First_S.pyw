import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class Login_Begin(GridLayout):
    def __init__(self,**kwargs):
        super(Login_Begin,self).__init__(**kwargs)
        self.cols=2
        self.add_widget(Label(text='Buscar Archivo'))


class My_S1(App):
    def build(self):
        return Login_Begin()

if __name__=='__main__':
    My_S1().run()