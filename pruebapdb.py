import Bio
import os
from Bio.PDB import PDBList
'''Selecting structures from PDB'''
def getpdbfiles(List_ID):
    pdbl = PDBList()
    current_path = os.path.dirname(__file__)
    #os.makedirs(current_path+"/Proteins/")
    PDBlist2=List_ID
    cont=0
    f=""
    for i in PDBlist2:
        pdbl.retrieve_pdb_file(i, pdir=current_path, file_format='pdb')
        
        #pdbl.download_pdb_files(i, obsolete=False, pdir='PDB', file_format='pdb', overwrite=False)
        #if(cont==4):
            #f=""  
        #   pdbl.download_pdb_files (f, obsolete=False, pdir='PDB', file_format='pdb', overwrite=False)
        #   f=""  
        #   cont=0

    for i in PDBlist2:
        sl=i.lower()
        nombre_nuevo=current_path+"/"+sl+".pdb"
        archivo=current_path+"/pdb"+sl+".ent"
        os.rename(archivo, nombre_nuevo) 
        #f=f+i
        #cont=cont+1
        
        #