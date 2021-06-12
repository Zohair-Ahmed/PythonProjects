from os import closerange
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

# FUNCTIONS
def createTable(): # create csv file of Ontario cities
    url = "https://en.wikipedia.org/wiki/List_of_cities_in_Ontario" #URL
    response = requests.get(url)

    getPage = BeautifulSoup(response.text, 'html.parser') # get HTML page
    [s.extract() for s in getPage('sup')] # remove superscripts
    getTable = getPage.find('table', {'class': "wikitable"}) # get the table from the HTML page
    ontTable = pd.read_html(str(getTable)) # read the table

    global ontDataFrame
    ontDataFrame = pd.DataFrame(ontTable[0]) # convert table to dataframe
    ontDataFrame = ontDataFrame.drop(["Municipalstatus", "Census division"], axis=1) # drop the unwanted columns
    ontDataFrame = ontDataFrame.rename(columns={"Populationdensity": "Population Density"})
    ontDataFrame.to_csv('PythonProjects/AboutOntario/ontCitiesInfo.csv', index = False) # save to csv file

def aboutMyCity(): # get info about user input city
    usrCity = input("What is your city?\n")

    with open('PythonProjects/AboutOntario/ontCitiesInfo.csv', 'rt') as f:
        reader = csv.reader(f, delimiter = ',')
        for row in reader:
            if usrCity == row[0]:
                print(row[0])
                return
        print(usrCity + " is not a city in Ontario. Try again!")
        


# MAIN METHOD
createTable()
print("\nWelcome to AboutOntario!")
actions = "\nWhat do you want to know about Ontario?\n\t1 - Everything\n\t2 - My City\n\t3 - Compare Cities\n\t0 - Exit\n"
getAction = input(actions)
getAction = int(getAction)

while getAction != 0:
    if getAction == 1:
        print(ontDataFrame)
    if getAction == 2:
        aboutMyCity()
    
    getAction = input(actions)
    getAction = int(getAction)  

print("\nSee ya later, eh!")