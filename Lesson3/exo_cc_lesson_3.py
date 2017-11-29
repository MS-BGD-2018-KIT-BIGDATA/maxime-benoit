import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import math


# renvoie un dictionnaire (nom,réduction(%))
def get_reducs(marque, nb_pages):

    reduc = {}

    for page in range(1, nb_pages+1):

        url = "https://www.cdiscount.com/search/10/ordinateur+portable+" + \
            marque + ".html?&page=" + str(page)+"&_his_#_his_"
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')
        containers = soup.find_all("div", class_="prdtBloc")

        for container in containers:

            if(len(container.find_all("div", class_='prdtPrSt')) > 0):
                name = container.find_all(class_='prdtBTit')[0].text

                try:
                    old_price = float(container.find_all(class_='prdtPrSt')
                                      [0].text.replace(',', '.'))
                    new_price = float(container.find_all(
                        class_='prdtPrice')[0].text.replace('€', '.'))
                    reduc[name] = math.floor(
                        (new_price-old_price)/old_price*10000)/100
                except ValueError:
                    pass

    return reduc

# print le resultat de get_reduc (avec la somme des pourcentages en
# premier pour une vue globale)
def print_reducs(reduc):
    print('total : ' + str(sum(reduc.values())) + ' %\n')
    print('nb of reduc : ' + str(len(reduc)) + '\n')
    print('mean : ' + str(sum(reduc.values())/len(reduc)) + ' %\n')
    print('\n')
    print("{:<65} {:<8}".format('Name', 'Reduc'))
    for k, v in reduc.items():
        print("{:<65} {:<8}".format(k, v) + " %")


# tests sur 5 pages pour dell, acer, hp, lenovo, apple
print("\nDELL :\n")
print_reducs(get_reducs('dell', 5))

print("\nACER :\n")
print_reducs(get_reducs('acer', 5))

print("\nHP :\n")
print_reducs(get_reducs('hp', 5))

print("\nLENOVO :\n")
print_reducs(get_reducs('lenovo', 5))

print("\nAPPLE :\n")
print_reducs(get_reducs('apple', 5))
