from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tweepy
import time
import credentials
import json

#getting the last tweeted tiktok link from the json file
with open('data.json', 'r') as f:
    data = json.load(f)
    latest_tiktok = (data["link"])

#tweepy auth
auth = tweepy.OAuth1UserHandler(credentials.API_KEY, credentials.API_KEY_SECRET,credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.tiktok.com/@le_sserafim?lang=en")

div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tiktok-yvmafn-DivVideoFeedV2")))

len = 0

for i in range(1, 100):
    xpath = "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[1]/div/div/a"
    link = div.find_element(By.XPATH, xpath).get_attribute("href")
    if (link==latest_tiktok):
        break
    len+=1

for i in range(len, 0, -1):
    xpath = "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[1]/div/div/a"
    link = div.find_element(By.XPATH, xpath).get_attribute("href")
    tweet = "[TikTok Update - date] (" + link + ")" "\n\n#LE_SSERAFIM"
    # api.update_status(status=link)
    if i == 1:
        with open('data.json', 'w') as outfile:
            data = { "link": link }
            json.dump(data, outfile)