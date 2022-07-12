from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import strftime
from urllib.parse import urlparse
import tweepy
import credentials
import pickle
import time
import urllib.request as dl
import requests
import os
import json
import re

import tiktok
import instagram

#to report errors
def errorDM(class_name, e):  
    # tweepy.send_direct_message(recipient_id=credentials.RECIPIENT_ID, text="Error with " + str(class_name) + "/nError: " + str(e))
    print("Error with " + str(class_name) + "/nError: " + str(e))

#to combine audio and video with instagram videos
def combine_audio(vidname, audname, outname):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=25)
    time.sleep(5)
    os.replace(outname, vidname)
    os.remove(audname)

#tweepy auth
auth = tweepy.OAuth1UserHandler(credentials.API_KEY, credentials.API_KEY_SECRET,credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#selenium
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)