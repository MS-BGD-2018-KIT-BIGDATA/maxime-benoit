
# LEBONCOIN.FR
# Renault zoé occasion Ile de France, PACA et Aquitaine

# version (ZEN, INTENS, LIFE)

# année
# kilométrage
# prix

# téléphone du propriétaire
# professionnel / particulier

# http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.
# prix de l'argus

# prix plus ou moins cher que cote moyenne

import requests
from bs4 import BeautifulSoup
import json
import math
import operator
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import re

# get soup from url

def get_soup(url):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

# get links annonces

def get_links(region, pro_part):
    page = 1
    links = []

    while(True):

        # get soup
        url = "https://www.leboncoin.fr/voitures/offres/" + region + "/?o=" + \
            str(page) + "&q=Renault%20Zo%E9%20&f=" + pro_part

        soup = get_soup(url)

        # break si page vide
        if soup.select("section.tabsContent.block-white.dontSwitch") == []:
            break

        # entrer dans le tableau d'annonce et extraction des annonces
        tab = soup.select("section.tabsContent.block-white.dontSwitch")[0]
        annonces = tab.select("a.list_item.clearfix.trackable")

        for annonce in annonces:
            links.append("http:" + annonce.get('href'))

        page += 1

    return links

# get values from javascript data

def get_value_from_script(data, key):
    key_index = data.find(key + " :")
    value_index = data.find(":", key_index)+3
    value_index_end = data.find("\"", value_index)
    return data[value_index:value_index_end]

# get phone number from text

def get_phone_number(text):
    text = text.replace('.', '')
    text = text.replace(' ', '')
    text = text.replace('-', '')

    try:
        regex = '(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}'
        phone = re.findall(regex, text)[0]
        return phone
    except:
        return 'NaN'

# 0 ################# INITIALIATION

pro_parts = ['c', 'p']
regions = ['provence_alpes_cote_d_azur', 'aquitaine', 'ile_de_france']
versions = ['zen', 'intens', 'life']

# 1 ################# GET ARGUS MOYEN PAR VERSION

soup = get_soup(
    "http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html")

modeles = soup.select("div.listingResultLine.auto")


def get_argus(lien):
    soup = get_soup(lien)
    argus = soup.select("div.boxQuotTitle")[0].select(
        "span.jsRefinedQuot")[0].text
    argus = float(argus.replace(' ', ''))
    return argus


def get_version(text):
    version = 'Nan'
    for v in versions:
        if v in text:
            version = v
            break
    return version


i = 1
df_argus = pd.DataFrame(columns=['version', 'argus'])

for modele in modeles:

    lien = "http://www.lacentrale.fr/" + modele.find("a").get("href")
    version = get_version(modele.text.lower())
    argus = get_argus(lien)
    df_argus.loc[i] = [version, argus]
    i += 1


df_argus = df_argus.groupby('version').mean()

argus_dict = df_argus.to_dict()['argus']

# 2 ################# GET AUTRES INFOS

i = 1
df = pd.DataFrame(columns=['link', 'region', 'version', 'year', 'km',
                           'price', 'tel', 'pro_part'])
for region in regions:

    print(region)

    for pro_part in pro_parts:

        annonces = get_links(region, pro_part)

        for annonce in annonces:

            print(annonce)

            soup = get_soup(annonce)

            # prix, annee, km (from javascript)

            data = soup.find_all("body")[0].findAll("script")[3].text

            prix = int(get_value_from_script(data, "prix"))
            annee = int(get_value_from_script(data, "annee"))
            km = int(get_value_from_script(data, "km"))

            # version, tel (from text)

            description = soup.select(
                "div.line.properties_description")[0].text
            titre = soup.select("header.adview_header.clearfix")[
                0].select("h1")[0].text
            text = (titre + ' ' + description).lower()

            version = get_version(text)
            tel = get_phone_number(text)

            # stockage des données

            df.loc[i] = [annonce, region, version, annee,
                         km, prix, tel, pro_part]
            print(df.loc[i])
            i += 1

# 2 ################# MERGE DES DATAFRAME ET COMPARAISON DES PRIX/ARGUS

df['argus'] = df['version'].map(argus_dict)
df['is_below_argus'] = df['price'] < df['argus']

print(df)

df.to_csv('/Users/maxime/Desktop/renaultzone.csv')
