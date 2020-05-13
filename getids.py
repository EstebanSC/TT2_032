import requests
import os
from pypdb import find_results_gen
import time
import pprint
def getIDPDB(item):

    url = 'http://www.rcsb.org/pdb/rest/search'
    query_text ='<?xml version="1.0" encoding="UTF-8"?> <orgPdbQuery> <queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType> <description>Text Search for: '+ item +'</description><keywords>' + item +'</keywords></orgPdbQuery>'

    #print("Query: %s" % query_text)
    print("Querying RCSB PDB REST API...")

    header = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, data=query_text, headers=header)

    if response.status_code == 200:
            #print("Found %d PDB entries matching query." % len(response.text))
            #print("Matches: \n%s" % response.text)
            Ids=response.text.split()
            #print(Ids[0])
            return Ids[0]
    else:
            print("Failed to retrieve results")

def getbest(item):
        check=""        
        name=item
        #coincidence=[]
        #coin=False

        print(name)
        #time.sleep(3)
        
        try:
                #print("Entra al try")
                result_gen =find_results_gen(name)
                if(result_gen=="None"):
                        print("None")
                for item in result_gen:
                        #print(item)
                        check= str(item)
                        #name=name.upper
                        if check.find(name)== 0:
                                #coincidence.append(check)
                                coin=True
                                #print(check)
                                break
                        #else:
                        #    print("Se encontraron proteinas sin coincidencias")
                #pprint.pprint([item for item in result_gen][:2])
                
                if(coin):
                        #print("Mejor proteina:" + coincidence[0])
                        print(check)
                        return(check)
                        #return coincidence[0]
                else:
                        #error="Se encontraron proteinas sin coincidencias"
                        error="402"
                        print(error)
                        return error
        except:
        #error="Compuesto inexistennte"
               
                error="403"
                print(error)
                return error