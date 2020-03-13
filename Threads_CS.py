import threading
import time 
from Screen import *
from LectCI import *


####################En esta funcion se mandan a llamar las funciones donde se obtiene info de cada DB
def get_data(compounds, proteins,project_path):
    search_r()
    connect_DrugBank(compounds,project_path)
    connect_PDB(proteins,project_path)
##################################################