from selenium import webdriver
from selenium.common.exceptions import TimeoutException

PATH = "/Users/Zohair/chromedriver.exe"
url = "https://www.facebook.com"

from selenium import webdriver
driver = webdriver.Chrome(PATH)
driver.get(url)

username = driver.find_element_by_id("email")
password = driver.find_element_by_id("pass")
submit = driver.find_element_by_id("loginbutton")

username.send_keys("zohair.a99@gmail.com")

submit.click()
