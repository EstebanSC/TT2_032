from pypdb import find_results_gen
import pprint

#def getbest():
check=""
name="Coronin"
coincidence=[]
coin=False
try:
    result_gen =find_results_gen(name)
    #pprint.pprint([item for item in result_gen][:10])
    #for item in result_gen:
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
        #return coincidence[0]
    else:
        #error="Se encontraron proteinas sin coincidencias"
        error="403"
        #return error
        print("Se encontraron proteinas sin coincidencias")
except:
    #error="Compuesto inexistennte"
    print("Compuesto inexistente")
    error="402"
    #return error