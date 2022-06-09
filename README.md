# election_scraper
This script is written to scrape data from website of Czech statistical office https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ and it is writen in python.
List of external packages (requests and bs4) is inclued in file requirements.txt.
Name of the script is Election_scraper.py and it designed to be launched from command prompt.
Script collects information about results of parliamentary election in Czechia in 2017 from every city of selected county (okres).
Output data has .csv format and each row contains name of the city, city number, number of voters, number of issued envelopes, number of valid votes and candidating parties.
Script is launched by two system arguments.
First argument is url adress of county you want to scrape (be careful to input url in "" brackets).
Second argument is a name of output .csv file.
Example of output file for Prostějov county is included in this folder.
