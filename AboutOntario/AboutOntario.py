from os import closerange
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

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


def aboutMyCity():  # get info about user input city
    usrCity = input("What is your city?\n")

    with open('PythonProjects/AboutOntario/ontCitiesInfo.csv', 'rt') as f:
        reader = csv.reader(f, delimiter=',')
        i = -1 # row counter
        for row in reader:
            if usrCity == row[0]:
                print("\nWhat do you want to know about " + usrCity + "?\n")
                cityCmmnd = "\t1 - Population(2016)\n\t2 - Population(2011)\n\t3 - Change In Population from 2011 to 2016(%)\n\t4 - Area(km²)\n\t5 - Population Density\n\t6 - All the Above\n\n"
                action = input(cityCmmnd)
                action = int(action)

                if action == 1:
                    print("\nPopulation(2016): " + row[1])
                elif action == 2:
                    print("\nPopulation(2011): " + row[2])
                elif action == 3:
                    print("\nChange In Population from 2011 to 2016(%): " + row[3])
                elif action == 4:
                    print("\nArea(km²): " + row[4])
                elif action == 5:
                    print("\nPopulation Density: " + row[5])
                elif action == 6:
                    print("\n" + str(ontDataFrame.loc[i, :]))
                else:
                    print("\nOption " + str(action) + " not available.")
                return
            i += 1

        print(usrCity + " is not a city in Ontario. Try again!")

def compareCities():
    city1 = input("Select City 1:\n")
    city1 = str(city1)

    # with open('PythonProjects/AboutOntario/ontCitiesInfo.csv', 'rt') as f:
    #     reader = csv.reader(f, delimiter=',')
    #     for row in reader:
          

    city2 = input("Select City 2:\n")


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

    getAction = input(actions)
    getAction = int(getAction)

print("\nSee ya later, eh!")
