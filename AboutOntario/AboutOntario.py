from os import closerange
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_cities_in_Ontario" #URL
tableClass = "wikitable sortable jquery-tablesorter"
response = requests.get(url)

getPage = BeautifulSoup(response.text, 'html.parser') # get HTML page
getTable = getPage.find('table', {'class': "wikitable"}) # get the table from the HTML page
ontTable = pd.read_html(str(getTable)) # read the table
df = pd.DataFrame(ontTable[0]) # convert table to dataframe

# drop the unwanted columns
data = df.drop([], axis=1)
# rename columns for ease
data = data.rename(columns={"Name[1][8]": "Name", "Census division[1][9]": "Census Division", "Population(2016)[2]": "Population (2016)",
                            "Population(2011)[8]": "Population (2011)", "Change(%)[8]": "Change(%)", "Area(km²)[8]": "Area(km²)", 
                            "Populationdensity[8]": "Population Density"})

print(data)