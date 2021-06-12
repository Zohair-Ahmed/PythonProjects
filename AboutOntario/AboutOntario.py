from os import closerange
import pandas as pd
import requests
from bs4 import BeautifulSoup

def createTable():
    url = "https://en.wikipedia.org/wiki/List_of_cities_in_Ontario" #URL
    response = requests.get(url)

    getPage = BeautifulSoup(response.text, 'html.parser') # get HTML page
    [s.extract() for s in getPage('sup')] # remove superscripts
    getTable = getPage.find('table', {'class': "wikitable"}) # get the table from the HTML page
    ontTable = pd.read_html(str(getTable)) # read the table

    ontDataFrame = pd.DataFrame(ontTable[0]) # convert table to dataframe
    ontDataFrame = ontDataFrame.drop(["Municipalstatus", "Census division"], axis=1) # drop the unwanted columns
    ontDataFrame.to_csv('PythonProjects/AboutOntario/ontCitiesInfo.csv', index = False) # save to csv file

    print(ontDataFrame)

createTable()