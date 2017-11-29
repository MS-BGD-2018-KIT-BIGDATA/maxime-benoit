import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# retourne un dataframe contenant les valeurs des comptes A,B,C, et D pour
# une année year


def GetComptesABCD(year):

    # extraction du fichier html
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + \
        str(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # valeurs de libelles
    libelles_h = ['A', 'B', 'C', 'D']
    libelles_v = ['En milliers dEuros',
                  'Euros par habitant', 'Moyenne de la strate']

    # montants correspondants
    montants = [montant.text.strip()
                for montant in soup.find_all(class_="montantpetit G")]
    montants = [int(montant.replace(" ", "")) for montant in montants]
    montants = montants[:6]+montants[9:15]
    montants = np.reshape(montants, (4, 3))

    # mise en forme dans un dataframe
    df = pd.DataFrame(data=montants, index=libelles_h, columns=libelles_v)

    return df

# print des années 2010 à 2015
for year in range(2010, 2016):
    print("Comptes " + str(year) + " :")
    print("")
    print(GetComptesABCD(year))
    print("")
