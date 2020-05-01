import requests
import os

def getIDPDB(item):

    url = 'http://www.rcsb.org/pdb/rest/search'
    query_text ='<?xml version="1.0" encoding="UTF-8"?> <orgPdbQuery> <queryType>org.pdb.query.simple.AdvancedKeywordQuery</queryType> <description>Text Search for: '+ item +'</description><keywords>' + item +'</keywords></orgPdbQuery>'

    print("Query: %s" % query_text)
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