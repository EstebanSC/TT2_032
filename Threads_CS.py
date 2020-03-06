import threading
import time 
from Screen import *
from LectCI import *


####################En esta funcion se mandan a llamar las funciones donde se obtiene info de cada DB
def get_data(compounds):
    search_r()
    connect_DrugBank(compounds)
##################################################