from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "/Users/Zohair/chromedriver.exe"
url = "https://en.wikipedia.org/wiki/List_of_cities_in_Ontario"

driver = webdriver.Chrome(PATH)
driver.get(url)