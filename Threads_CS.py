import threading
import time 
from Screen import *
from LectCI import *

#logging.basicConfig( level=logging.DEBUG,
 #   format='[%(levelname)s] - %(threadName)-10s : %(message)s')#Se deben implementar hilos, pero al hacer DEBUG, son
    #Necesarios

def get_data(compounds):
    search_r()
    #pantalla=threading.Thread(target=search_r,name='PantallaDatos')
    #connect=threading.Thread(target=connect_DrugBank(compounds), name='getDataDB')
    #pantalla.setDaemon(True)
    #connect.setDaemon(True)
    #pantalla.start()
    #connect.start()