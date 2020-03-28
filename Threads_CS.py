import threading
import time 
from Screen import *
from LectCI import *


####################En esta funcion se mandan a llamar las funciones donde se obtiene info de cada DB
def get_data(compounds, proteins,project_path):
    #search_r()
    w=WaitSearchData()
    w.ver(compounds,proteins,project_path)
    #CDB= threading.Thread(target=connect_DrugBank(compounds,project_path))
    #CDB.start()
    #W=threading.Thread(target=WaitSearchData()) 
    #connect_DrugBankBA(compounds,project_path)
    #connect_PDB(proteins,project_path)
##################################################