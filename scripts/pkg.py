from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import strftime
from resources.credentials import *
import tweepy
import pickle
import time
import urllib.request
import requests
import os
import json
import re

import tiktok
import instagram

#tweepy auth
auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#selenium
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#to report errors
def errorDM(class_name, e):  
    # tweepy.send_direct_message(recipient_id=credentials.RECIPIENT_ID, text="Error with " + str(class_name) + "/nError: " + str(e))
    print(
        type(e).__name__,          
        __file__,                  
        e.__traceback__.tb_lineno,
        e
    )
    # print("Error with " + str(class_name) + "/nError: " + str(e))

#to combine audio and video with instagram videos
def combine_audio(vidname, audname, outname):
    vidname = "download\\" + str(vidname)
    audname = "download\\" + str(audname)
    outname = "download\\" + str(outname)
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=25)
    time.sleep(5)
    os.replace(outname, vidname)
    os.remove(audname)

def download(url, name, ftype):
    urllib.request.urlretrieve(str(url), ("downloads\\" + str(name) + "." + str(ftype)))

def media_upload(filename):
    try:
        upload_result = api.media_upload("downloads\\" + str(filename) + ".png")
    except:
        upload_result = api.media_upload("downloads\\" + str(filename) + ".mp4")
    return upload_result

def update_status(sRange, eRange, tweettext):
    for i in range(int(sRange), int(eRange)):
        upload_result = media_upload(i)
        files.append(upload_result.media_id_string)

    tweetR= api.update_status(status=tweettext, media_ids=files)
    upload_result=""
    files = []

    return tweetR

def update_status_thread(sRange, eRange, tweettext, tweet):
    for i in range(int(sRange), int(eRange)):
        upload_result = media_upload(i)
        files.append(upload_result.media_id_string)

    tweetR= api.update_status(status=tweettext, media_ids=files, in_reply_to_status_id=tweet.id)
    upload_result=""
    files = []

    return tweetR

def get_data(index):
    with open('scripts\\resources\\data.json', 'r') as outfile:
        data = json.load(outfile)
        latest_link = (data[index])
        outfile.close()
        return latest_link

def update_data(index, value):
    with open('scripts\\resources\\data.json', 'r+') as outfile:
            data = json.load(outfile)
            data[index] = value
            outfile.seek(0)
            json.dump(data, outfile, indent=4)
            outfile.truncate()

def instagram_login():
    try:
        cookies = pickle.load(open("scripts\\resources\\cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.get("https://www.instagram.com/")

    except:
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]")))
        username = driver.find_element(By.NAME, "username")
        username.send_keys(INSTAGRAM_USERNAME)
        password = driver.find_element(By.NAME, "password")
        password.send_keys(INSTAGRAM_PASSWORD)
        driver.find_element(By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]").click()
        logindone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div/div/section/div/button")))
        pickle.dump( driver.get_cookies() , open("resources\\cookies.pkl","wb"))