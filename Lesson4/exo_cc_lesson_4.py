# open-med

# ibuprophène

# labos, equivalent traietement = dosage * nombre de comprimés, année de commercialisation
# mois, prix, restriction age, restriction poids


import requests
from bs4 import BeautifulSoup
import json
import math
import operator
import pandas as pd

page = 1


# get codes

code_ics = []
while (page == 1):

    api = 'https://open-medicaments.fr/api/v1/medicaments?query=ibuprofene&page=' + \
        str(page) + '&api_key=ibuprof%C3%A8ne'
    json_content = requests.get(api).text
    content = json.loads(json_content)

    if content == []:
        break

    code_ics += [int(data['codeCIS']) for data in content]

    page += 1

# get infos

df = pd.DataFrame(columns=['labo', 'annee', 'mois', 'prix',
                           'composition(g)'])

i = 1
for medicament in code_ics:

    api = 'https://open-medicaments.fr/api/v1/medicaments/' + str(medicament)
    json_content = requests.get(api).text
    data = json.loads(json_content)

    labo = data['titulaires'][0]
    annee = data['dateAMM'][:4]
    mois = data['dateAMM'][5:7]
    prix = data['presentations'][0]['prix']
    composition = data['compositions'][0][
        'substancesActives'][0]['dosageSubstance'][0]

    df.loc[i] = [labo, annee, mois, prix, composition]
    i += 1

print(df)
