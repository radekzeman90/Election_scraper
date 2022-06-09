"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Radek Zeman
email: ze.ra@seznam.cz
discord: Radek Zeman
"""
import requests
import bs4
import csv
import sys

def city_adress_list(adress):
    """
    Tato funkce vrátí list adres, kdy každá adresa
    obsahuje volební výsledky v jedné obci zvoleného okresu.
    This function returns list of adresses, where each adress
    contains election results of single city in chosen county.
    """
    list_of_adresses = list()
    cities = requests.get(adress)
    soup1 = bs4.BeautifulSoup(cities.text, "html.parser")
    tables = soup1.select('a')
    for link in tables:
        if link.get_text().isnumeric():
            list_of_adresses.append('https://volby.cz/pls/ps2017nss/'+link.get('href'))
    return(list_of_adresses)

def election_scraper(adress):
    """
    Tato funkce vyscrapuje požadované volební výsledky
    ze stránky dané obce.
    This function scrapes required election results
    from given city's webpage.
    """
    getr = requests.get(adress)
    soup = bs4.BeautifulSoup(getr.text, "html.parser")
    parties = list()
    voters_in_list = soup.find('td', {'class':'cislo', 'headers':'sa2'}).text
    issued_envelopes = soup.find('td', {'class':'cislo', 'headers':'sa3'}).text
    valid_votes = soup.find('td', {'class':'cislo', 'headers':'sa6'}).text
    party_scrape1 = soup.find_all('td',  {'class':'overflow_name', 'headers':'t1sa1 t1sb2'})
    party_scrape2 = soup.find_all('td',  {'class':'overflow_name', 'headers':'t2sa1 t2sb2'})
    start, end = 'obec=', '&xvyber'
    city_number = adress.split(start)[1].split(end)[0]
    for word in party_scrape1:
        parties.append(word.text)
    for word in party_scrape2:
        parties.append(word.text)
    h3 = soup.find_all('h3')
    for word in h3:
        if 'Obec:' in word.string:
            city_name = word.text.replace('Obec: ', '').replace('\n', '')
    return city_name, city_number, voters_in_list, issued_envelopes, valid_votes, parties

def create_csv(adress, file_name):
    """
    Tato funkce vytvoří a uloží soubor ve formátu .csv,
    který bude obsahovat požadovaná data o volebních výsledcích
    v daném okrese.
    This function creates and save .csv file, which contains
    required data of election results in given county.
    """
    list_of_adresses = city_adress_list(adress)
    new_csv = open(f"{file_name}.csv", mode = "w", newline = "")
    writer = csv.writer(new_csv)
    writer.writerow(('city name', 'city number', 'voters in list', 'issued envelopes', 'valid votes', 'candidating parties'))
    for adress in list_of_adresses:
        result = election_scraper(adress)
        writer.writerow(result)
    new_csv.close()

# If launched from command prompt, first argument is county's webpage adress
# and second argument is output file's name.

if len(sys.argv) != 3:
    print('Wrong number of input arguments.')
    quit()
else:
    pass

if not 'volby.cz/pls/ps2017nss' in str((sys.argv[1])):
    print('Incorrect adress, please enter the right one.')
    quit()
else:
    pass

if 'volby.cz/pls/ps2017nss' in str((sys.argv[2])):
    print('You have confused adress and file name arguments')
    quit()
else:
    pass

if __name__ == '__main__':
    create_csv(sys.argv[1], sys.argv[2])
