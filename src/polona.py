import requests
import json
import os
current_dir = os.path.dirname(__file__)

def PolonaGetFirst(title:str):
    #Find entity id by request
    URL='https://polona.pl/api/entities/'
    PARAMS={'query':title, 'size':'1', 'public':'1'}

    r = requests.get(URL, PARAMS)
    data = r.json()
    e_id = data['hits'][0]['id']
    return e_id


#Returns list of scans for a given title in polona
def PolonaScan(title:str):
    e_id = PolonaGetFirst(title)

    #Get data of an entity
    URL='https://polona.pl/api/entities/'+e_id+'/'

    r = requests.get(URL,None)
    data = r.json()

    scanlist = list()
    for i in data['scans']:
        scanlist.append(str(i['resources'][0]['url']))
    
    return scanlist

#Returns a slug name for a searched title
def PolonaSlug(title:str):
    e_id = PolonaGetFirst(title)

    #Get data of an entity
    URL='https://polona.pl/api/entities/'+e_id+'/'

    r = requests.get(URL,None)
    data = r.json()
    
    return data['slug']

def PolonaScanIsPublic(title:str):
    URL='https://polona.pl/api/entities/'
    PARAMS={'query':title, 'size':'1', 'public':'1'}

    r = requests.get(URL, PARAMS)
    data = r.json()
    e_id = data['hits'][0]['id']

    URL='https://polona.pl/api/entities/'+e_id+'/'
    r = requests.get(URL, {})
    data = r.json()
    return data['is_public']