# IMPORT STATEMENTS
from os import closerange
import pandas as pd
import requests
from requests.api import get
from bs4 import BeautifulSoup
import csv

# GLOBAL VARIABLES
cityCmmnd = "\t1 - Population(2016)\n\t2 - Population(2011)\n\t3 - Change In Population from 2011 to 2016(%)\n\t4 - Area(km²)\n\t5 - Population Density\n\t6 - All the Above\n\t0 - Exit\n\n"

# FUNCTIONS
def createTable():  # create csv file of Ontario cities
    url = "https://en.wikipedia.org/wiki/List_of_cities_in_Ontario"  # URL
    response = requests.get(url)

    getPage = BeautifulSoup(response.text, 'html.parser')  # get HTML page
    [s.extract() for s in getPage('sup')]  # remove superscripts
    # get the table from the HTML page
    getTable = getPage.find('table', {'class': "wikitable"})
    ontTable = pd.read_html(str(getTable))  # read the table

    global ontDataFrame
    ontDataFrame = pd.DataFrame(ontTable[0])  # convert table to dataframe
    ontDataFrame = ontDataFrame.drop(
        ["Municipalstatus", "Census division"], axis=1)  # drop the unwanted columns
    ontDataFrame = ontDataFrame.rename(
        columns={"Populationdensity": "Population Density"})
    # save to csv file
    ontDataFrame.to_csv(
        'PythonProjects/AboutOntario/ontCitiesInfo.csv', index=False)

def searchCity(city):  # city -> usr input, see if city exists
    with open('PythonProjects/AboutOntario/ontCitiesInfo.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        i = -1  # row counter
        for row in reader:
            if city == row[0]:
                return i
            i += 1
        return -1

def theAction(action, usrCity, cityRow): # prints the output based on the user input
    if action == 1:
        return "\n" + usrCity +"'s Population(2016): " + str(ontDataFrame.loc[cityRow, "Population(2016)"])
    elif action == 2:
        return "\n" + usrCity +"'s Population(2011): " + str(ontDataFrame.loc[cityRow, "Population(2011)"])
    elif action == 3:
        return "\n" + usrCity +"'s Change In Population from 2011 to 2016(%): " + str(ontDataFrame.loc[cityRow, "Change(%)"])
    elif action == 4:
        return "\n" + usrCity +"'s Area(km²): " + str(ontDataFrame.loc[cityRow, "Area(km²)"])
    elif action == 5:
        return "\n" + usrCity +"'s Population Density: " + str(ontDataFrame.loc[cityRow, "Population Density"])
    elif action == 6:
        print("\n" + str(ontDataFrame.loc[cityRow, :]))
    else:
        print("\nOption " + str(action) + " not available.")

def aboutMyCity():  # get info about user input city
    usrCity = input("What is your city?\n")
    cityRow = searchCity(usrCity)

    if cityRow == -1:
        print("Unfortunately, there is no documentation on " + usrCity)
    else:
        print("\nWhat do you want to know about " + usrCity + "?\n")
        action = input(cityCmmnd)
        action = int(action)

        while action != 0:
            print(theAction(action, usrCity, cityRow))
            print("\nWhat do you want to know about " + usrCity + "?\n")
            action = input(cityCmmnd)
            action = int(action)

def selectCity(cityNum):
    city = input("\nSelect City " + str(cityNum) + ":\n")
    city = str(city)
    cityRow = searchCity(city)

    while cityRow == -1:
        print("Unfortunately, there is no documentation on " + city + ". Try again.")
        city = input("\nSelect City 1:\n")
        city = str(city)
        cityRow = searchCity(city)
    
    return city

def compareCities(): # compare two cities specified by the user input
    city1 = selectCity(1)
    city1Row = searchCity(city1)
    city2 = selectCity(2)
    city2Row = searchCity(city2)

    print("\nWhat do you want to know about these cities?\n")
    action = input(cityCmmnd)
    action = int(action)

    while action != 0:
        print(theAction(action, city1, city1Row)) # info about city 1
        print(theAction(action, city2, city2Row)) # info about city 2

        print("\nWhat do you want to know about these cities?\n")
        action = input(cityCmmnd)
        action = int(action)

# MAIN METHOD
createTable()
print("\nWelcome to AboutOntario!")
actions = "\nWhat do you want to know about Ontario?\n\t1 - Everything\n\t2 - My City\n\t3 - Compare Cities\n\t0 - Exit\n"
getAction = input(actions)
getAction = int(getAction)

while getAction != 0:
    if getAction == 1:
        print(ontDataFrame)
    elif getAction == 2:
        aboutMyCity()
    elif getAction == 3:
        compareCities()
    else:
        print("\nOption " + str(getAction) + " not available.")

    getAction = input(actions)
    getAction = int(getAction)

print("\nSee ya later, eh!") # if 0 is entered