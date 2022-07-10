from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import strftime
from instascrape import Reel
import time
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

#to report errors
def errorDM(class_name, e):  
    # tweepy.send_direct_message(recipient_id=credentials.RECIPIENT_ID, text="Error with " + str(class_name) + "/nError: " + str(e))
    print("Error with " + str(class_name) + "/nError: " + str(e))

def tiktok():

    try:
        #getting the last tweeted tiktok link from the json file
        with open('data.json', 'r') as f:
            data = json.load(f)
            latest_tiktok = (data["tiktokLink"])

        driver.get("https://www.tiktok.com/@aespa_official")

        #waits until the page loads
        div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div")))

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
            div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div")))
            link = div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[1]/div/div/a").get_attribute("href")
            bio = div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[2]/a").get_attribute("title")
            
            #fixing hashtags
            biotext = bio.split("#")
            if re.findall('with', bio):
                biotext[0] = biotext[0] + "#" + biotext[1]
                
            if re.findall("@", bio):
                biotemp = biotext[0].split("@")
                biotext[0] = biotemp[0] + "@/" + biotemp[1]

            hashtaglist = "#KARINA", "#카리나", "#GISELLE", "#지젤", "#WINTER", "#윈터", "#NINGNING", "#닝닝"
            hashtags = ""
            for hashtag in hashtaglist:
                if re.findall(hashtag, bio):
                    hashtags = hashtags + " " + hashtag
            
            #downloading the video
            driver.get(div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[1]/div/div/a").get_attribute("href"))
            div1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[1]/div[2]/div/div/div")))
            videolink = div1.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[1]/div[2]/div/div/div/video").get_attribute("src")
            urllib.request.urlretrieve(videolink, 'tiktok.mp4')

            #tweeting
            tweet = "[TikTok Update - " + str(strftime("%d%m%y")) + "] (" + link + ")" + "\n\n" + " ".join(biotext[0].strip().split()) + "\n\n#aespa #에스파" + hashtags
            upload_result = api.media_upload('tiktok.mp4')
            api.update_status(status=tweet, media_ids=[upload_result.media_id_string])
            os.remove('tiktok.mp4')
            upload_result=""
            
            #posting the new link to the json file for the next run
            if i == 1:
                with open('data.json', 'r+') as outfile:
                    data = json.load(outfile)
                    data['tiktokLink'] = link
                    outfile.seek(0)
                    json.dump(data, outfile, indent=4)
                    outfile.truncate()
            
            driver.get("https://www.tiktok.com/@aespa_official")
    
    except Exception as e:
        errorDM("tiktok", e)

def instagram():

    # try:
        driver.get("https://www.instagram.com/")

        #login to instagram
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]")))
        username = driver.find_element(By.NAME, "username")
        username.send_keys(credentials.INSTAGRAM_USERNAME)
        password = driver.find_element(By.NAME, "password")
        password.send_keys(credentials.INSTAGRAM_PASSWORD)
        driver.find_element(By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]").click()
        logindone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div/div/section/div/button")))

        i=1
        profilelink = "https://www.instagram.com/aespa_official"

        #getting the last tweeted instagram link from the json file
        with open('data.json', 'r') as f:
            data = json.load(f)
            latest_link = (data["instagramLink"])
            i=i+1

        #go to the instagram page
        driver.get(profilelink)
        #waits until the page loads
        instagramPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_aa-i")))
        postRows = instagramPage.find_elements(By.CLASS_NAME, "_ac7v")
        newPosts=[]

        c=False

        #getting the new posts
        for postRow in postRows:
            posts = postRow.find_elements(By.CLASS_NAME, "_aabd")
            for post in posts:
                link = post.find_element(By.TAG_NAME, "a").get_attribute("href")
                if (link==latest_link):
                    break
                newPosts.append(link)
                c=True
            else:
                continue
            break

        if c == True:
            #tweeting the posts
            for newPost in newPosts:
                driver.get(newPost)
                caption=""
                len=0

                try:
                    singlepost = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_aato")))
                    link = singlepost.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div/div/div[1]/img").get_attribute("src")
                    urllib.request.urlretrieve(link, '1.png')
                    try:
                        caption = singlepost.find_element(By.XPATH, "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span").text
                        if re.findall("@", caption):
                            biotemp = caption.split("@")
                            caption = biotemp[0] + "@/" + biotemp[1]
                    except:
                        caption=""     

                except:
                    try:
                        multipost = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_acay")))  
                        posts = ""
                        links = ""

                        try:
                            for i in range(1, 10):
                                posts = driver.find_elements(By.CLASS_NAME, "_acaz")
                                driver.find_element(By.CLASS_NAME, "_aahi").click()
                        except:
                            pass

                        for post in posts:
                            try:
                                link = post.find_element(By.TAG_NAME, "img").get_attribute("src")
                                urllib.request.urlretrieve(link, str(i)+ ".png")
                                len=len+1
                            except:
                                SESSIONID = driver.get_cookie("sessionid")
                                SESSIONID = SESSIONID["value"]

                                headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
                                    Safari/537.36 Edg/79.0.309.43",
                                    "cookie": f'sessionid={SESSIONID};'
                                }
                                insta_reel = Reel(newPost)

                                insta_reel.scrape(headers=headers)
                                insta_reel.download(str(i)+ ".mp4")

                                len=len+1
                                                                    
                        try:
                            caption = multipost.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span").text
                            if re.findall("@", caption):
                                biotemp = caption.split("@")
                                caption = biotemp[0] + "@/" + biotemp[1]
                        except:
                            caption=""  

                    except:
                        try:
                            video = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_ab1c")))
                            link = video.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div/div/video").get_attribute("src")
                            urllib.request.urlretrieve(link, 'instagram.mp4')

                        except:
                            video = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_ab1c")))
                            link = video.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div/div/video").get_attribute("src")
                            urllib.request.urlretrieve(link, 'instagram.mp4')

                tweet = "[Instagram Update - " + str(strftime("%d%m%y")) + "] (" + link + ")" + "\n\n" + " " + caption + "\n\n#aespa #에스파"

                files = []

                if len <= 4:
                    for i in range(1, len+1):
                        try:
                            upload_result = api.media_upload(str(i) + ".png")
                        except:
                            upload_result = api.media_upload(str(i) + ".mp4")
                        files.append(upload_result.media_id_string)

                    api.update_status(status=tweet, media_ids=files)
                    upload_result=""

                elif len <= 8:
                    for i in range(1, 5):
                        try:
                            upload_result = api.media_upload(str(i) + ".png")
                        except:
                            upload_result = api.media_upload(str(i) + ".mp4")
                        files.append(upload_result.media_id_string)

                    tweet1 = api.update_status(status=tweet, media_ids=files)
                    upload_result=""
                    files = []

                    for i in range(5, len+1):
                        try:
                            upload_result = api.media_upload(str(i) + ".png")
                        except:
                            upload_result = api.media_upload(str(i) + ".mp4")
                        files.append(upload_result.media_id_string)

                    api.update_status(status=tweet, media_ids=files, in_reply_to_status_id=tweet1.id)
                    upload_result=""

                else:
                    for i in range(1, 5):
                        try:
                            upload_result = api.media_upload(str(i) + ".png")
                        except:
                            upload_result = api.media_upload(str(i) + ".mp4")
                        files.append(upload_result.media_id_string)

                    tweet1 = api.update_status(status=tweet, media_ids=files)
                    upload_result=""
                    files = []

                    for i in range(5, 9):
                        try:
                            upload_result = api.media_upload(str(i) + ".png")
                        except:
                            upload_result = api.media_upload(str(i) + ".mp4")
                        files.append(upload_result.media_id_string)

                    tweet2 = api.update_status(status=tweet, media_ids=files, in_reply_to_status_id=tweet1.id)
                    upload_result=""
                    files = []

                    for i in range(9, len+1):
                        try:
                            upload_result = api.media_upload(str(i) + ".png")
                        except:
                            upload_result = api.media_upload(str(i) + ".mp4")
                        files.append(upload_result.media_id_string)

                    api.update_status(status=tweet, media_ids=files, in_reply_to_status_id=tweet2.id)
                    upload_result=""
                    files = []

                for i in range(1, len+1):
                    try:
                        os.remove(str(i) + ".png")
                    except:
                        os.remove(str(i) + ".mp4")
                
                #posting the new link to the json file for the next run
                with open('data.json', 'r+') as outfile:
                    data = json.load(outfile)
                    data['instagramLink'] = link
                    outfile.seek(0)
                    json.dump(data, outfile, indent=4)
                    outfile.truncate() 

#tiktok()
instagram()

# if int(strftime("%M"))%10 == 0: