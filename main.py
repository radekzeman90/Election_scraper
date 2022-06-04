"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Radek Zeman
email: ze.ra@seznam.cz
discord: Radek Zeman
"""
import requests
import bs4
import csv

def adress_of_county(county):
    """
    Tato funkce vrátí adresu stránky okresu podle volby uživatele.
    """
    getr = requests.get('https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ')
    soup = bs4.BeautifulSoup(getr.text, "html.parser")
    pokus = soup.find('td', text = str(county))
    parent = pokus.parent
    sybling = parent.find('td', headers = "t12sa3")
    adress = sybling.find('a')
    county_adress = 'https://volby.cz/pls/ps2017nss/'+adress['href']
    return(county_adress)

def city_adress_list(adress):
    """
    Tato funkce vrátí list adres, kdy každá adresa
    obsahuje volební výsledky v jedné obci zvoleného okresu.
    """
    city_adress_list = list()
    obce = requests.get(adress)
    soup1 = bs4.BeautifulSoup(obce.text, "html.parser")
    table1 = soup1.find_all('td', {'headers':'t1sa1 t1sb1'})
    table2 = soup1.find_all('td', {'headers':'t2sa1 t2sb1'})
    table3 = soup1.find_all('td', {'headers':'t3sa1 t3sb1'})
    for slovo in table1:
      city_adress_list.append('https://volby.cz/pls/ps2017nss/'+str(slovo.find('a')['href']))
    for slovo in table2:
      city_adress_list.append('https://volby.cz/pls/ps2017nss/'+str(slovo.find('a')['href']))
    for slovo in table3:
      city_adress_list.append('https://volby.cz/pls/ps2017nss/'+str(slovo.find('a')['href']))
    return(city_adress_list)

def election_scraper(adress):
    """
    Tato funkce vyscrapuje požadované volební výsledky
    ze stránky dané obce.
    """
    getr = requests.get(adress)
    soup = bs4.BeautifulSoup(getr.text, "html.parser")
    parties = list()
    voters_in_list = soup.find('td', {'class':'cislo', 'headers':'sa2'}).text
    vydane_obalky = soup.find('td', {'class':'cislo', 'headers':'sa3'}).text
    platne_hlasy = soup.find('td', {'class':'cislo', 'headers':'sa6'}).text
    party_scrape1 = soup.find_all('td',  {'class':'overflow_name', 'headers':'t1sa1 t1sb2'},'\n')
    party_scrape2 = soup.find_all('td',  {'class':'overflow_name', 'headers':'t2sa1 t2sb2'},'\n')
    start, end = 'obec=', '&xvyber'
    city_number = adress.split(start)[1].split(end)[0]
    for slovo in party_scrape1:
        parties.append(slovo.text)
    for slovo in party_scrape2:
        parties.append(slovo.text)
    h3 = soup.find_all('h3')
    for word in h3:
        if 'Obec:' in word.string:
            city_name = word.text.replace('Obec: ', '').replace('\n', '')
    return city_name, city_number, voters_in_list, vydane_obalky, platne_hlasy, parties

def create_csv(adress, county):
    """
    Tato funkce vytvoří a uloží soubor ve formátu .csv,
    který bude obsahovat požadovaná data o volebních výsledcích
    v daném okrese.
    """
    adresa_okresu = adress_of_county(county)
    seznam_adres_mest = city_adress_list(adresa_okresu)
    new_csv = open("prvni_tabulkovy_soubor.csv", mode="w")
    writer = csv.writer(new_csv)
    writer.writerow(('city_name', 'city_number', 'voters_in_list', 'vydane_obalky', 'platne_hlasy', 'candidating_parties'))
    for adresa in seznam_adres_mest:
        result = election_scraper(adresa)
        writer.writerow(result)
    new_csv.close()

create_csv('http://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ', 'Prostějov')