from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import strftime
import tweepy
import credentials
import json
import re
import urllib.request
import os

#tweepy auth
auth = tweepy.OAuth1UserHandler(credentials.API_KEY, credentials.API_KEY_SECRET,credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#selenium
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def tiktok():

    #getting the last tweeted tiktok link from the json file
    with open('data.json', 'r') as f:
        data = json.load(f)
        latest_tiktok = (data["tiktokLink"])

    driver.get("https://www.tiktok.com/@le_sserafim")

    #waits until the page loads
    div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tiktok-yvmafn-DivVideoFeedV2")))

    #how many new tiktoks were made since the last check
    len = 0

    #getting len
    for i in range(1, 10):
        link = div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[1]/div/div/a").get_attribute("href")
        if (link==latest_tiktok):
            break
        len+=1

    #tweeting the new tiktoks
    for i in range(len, 0, -1):
        div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tiktok-yvmafn-DivVideoFeedV2")))
        link = div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[1]/div/div/a").get_attribute("href")
        bio = div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[2]/a").get_attribute("title")
        biotext = bio.split("#")

        #fixing hashtags
        if re.findall('with', bio):
            biotext[0] = biotext[0] + "#" + biotext[1]
            
        if re.findall('from', bio):
            if re.findall("@", bio):
                biotemp = biotext[0].split("@")
                biotext[0] = biotemp[0] + "@/" + biotemp[1]

        hashtaglist = "#CHAEWON", "#SAKURA", "#YUNJIN", "#KAZUHA", "#EUNCHAE", "#채원", "#사쿠라", "#윤진", "#카즈하", "#은채"
        hashtags = ""
        for hashtag in hashtaglist:
            if re.findall(hashtag, bio):
                hashtags = hashtags + " " + hashtag
        
        #downloading the video
        driver.get(div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[1]/div/div/a").get_attribute("href"))
        div1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tiktok-13egybz-DivBasicPlayerWrapper")))
        videolink = div1.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/div/video").get_attribute("src")
        urllib.request.urlretrieve(videolink, 'tiktok.mp4')

        #tweeting
        tweet = "[TikTok Update - " + str(strftime("%d%m%y")) + "] (" + link + ")" + "\n\n" + " ".join(biotext[0].strip().split()) + "\n\n#LE_SSERAFIM #르세라핌 #IMFEARLESS" + hashtags
        upload_result = api.media_upload('tiktok.mp4')
        api.update_status(status=tweet, media_ids=[upload_result.media_id_string])
        os.remove('tiktok.mp4')
        upload_result=""
        
        #posting the new link to the json file for the next run
        if i == 1:
            with open('data.json', 'w') as outfile:
                data = { "tiktokLink": link }
                json.dump(data, outfile)
        
        driver.get("https://www.tiktok.com/@le_sserafim")


tiktok()

# if int(strftime("%M"))%10 == 0:
    # tiktok()