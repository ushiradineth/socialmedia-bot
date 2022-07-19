from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import strftime
from resources.credentials import *
from os import walk
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
    vidname = "downloads\\" + str(vidname)
    audname = "downloads\\" + str(audname)
    outname = "downloads\\" + str(outname)
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=25)
    my_clip.close()
    os.replace(outname, vidname)
    os.remove(audname)

def download(url, name, ftype):
    urllib.request.urlretrieve(str(url), ("downloads\\" + str(name) + "." + str(ftype)))

def media_upload(filename):
    upload_result = ""
    try:
        upload_result = api.media_upload("downloads\\" + str(filename) + ".png")
    except:
        upload_result = api.media_upload("downloads\\" + str(filename) + ".mp4")
    return upload_result

def update_status(tweettext, lenn):
    if lenn == 1:
        files = []
        files.append(media_upload(1).media_id_string)
        tweet = api.update_status(status=tweettext, media_ids=files)
        files = []
    
    files = []
    tweet = ""
    filenames = next(walk("scripts\\downloads"), (None, None, []))[2]

    if lenn > 1:
        for i in range (1, 11):
            try:
                if (len(files) == 4):
                    if tweet != "":
                        tweetemp = api.update_status(status=tweettext, media_ids=files, in_reply_to_status_id=tweet.id)
                    else:
                        tweetemp = api.update_status(status=tweettext, media_ids=files)
                    tweet = tweetemp
                    files = []

                if str(i) + ".png" in filenames:
                    files.append(media_upload(1).media_id_string)

                elif str(i) + ".mp4" in filenames:
                    mp4temp = []
                    mp4temp.append(media_upload(1).media_id_string)
                    if tweet != "":
                        tweetemp = api.update_status(status=tweettext, media_ids=mp4temp, in_reply_to_status_id=tweet.id)
                    else:
                        tweetemp = api.update_status(status=tweettext, media_ids=mp4temp)
                    tweet = tweetemp
                    mp4temp = []
            except:
                pass

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

    except:
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]")))
        username = driver.find_element(By.NAME, "username")
        username.send_keys(INSTAGRAM_USERNAME)
        password = driver.find_element(By.NAME, "password")
        password.send_keys(INSTAGRAM_PASSWORD)
        driver.find_element(By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]").click()
        logindone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div/div/section/div/button")))
        pickle.dump( driver.get_cookies() , open("resources\\cookies.pkl","wb"))

def download_video(vlink, vidname):
    try:
        max = 0
        maxurl = ""
        min = 0
        minurl = ""

        urls = []
        x = 1

        time.sleep(5)

        for request in driver.requests:
            if request.response:
                try:
                    if request.url not in urls:
                        if (request.url).split("edm")[1].split("=")[1].split("&")[0] == str(vlink) and request.response.status_code == 200 and request.response.headers['Content-Type'].split("/")[0] == "video" and int(request.response.headers['Content-Length']) < 1000000:
                            r = requests.get(request.url.split("&bytestart")[0], stream=True)

                            if min == 0:
                                min = int(r.headers['Content-length'])

                            if int(r.headers['Content-length']) > max:
                                max = int(r.headers['Content-length'])
                                maxurl = r.url
                            elif int(r.headers['Content-length']) < min:
                                min = int(r.headers['Content-length'])
                                minurl = r.url      

                            urls.append(request.url)
                            x+=1
                            
                except Exception as e:
                    if str(e) != "list index out of range":
                        print(e)
                    pass

        try:
            download(maxurl, str(vidname), "mp4")

            try:
                download(minurl, str(vidname) + "audio", "mp4")
            except:
                combine_audio(str(vidname) + ".mp4", str(vidname) + ".mp4", "out.mp4")

            combine_audio(str(vidname) + ".mp4", str(vidname) + "audio.mp4", "out.mp4")

        except Exception as e:
            errorDM("instagram video donwload error: ", e)

    except Exception as e:
        errorDM("instagram video donwload error: ", e)