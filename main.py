from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import strftime
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
        profilelinks = "https://www.instagram.com/_chaechae_1/", "https://www.instagram.com/39saku_chan/", "https://www.instagram.com/k_a_z_u_h_a__/"

        for profilelink in profilelinks:
            #getting the last tweeted instagram link from the json file
            with open('data.json', 'r') as f:
                data = json.load(f)
                latest_link = (data["instagramLink" + str(i)])
                i=i+1

            #go to the instagram page
            driver.get(profilelink)
            #waits until the page loads
            instagramPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_aa-i")))
            postRows = instagramPage.find_elements(By.CLASS_NAME, "_ac7v")
            newPosts=""

            #getting the new posts
            for postRow in postRows:
                posts = postRow.find_elements(By.CLASS_NAME, "_aabd")
                for post in posts:
                    link = post.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if (link==latest_link):
                        break
                    print("link: ", link)
                    newPosts = newPosts + link
                else:
                    continue
                break

            print("newPosts: ", newPosts)
            newPosts = tuple(newPosts)
            print("newPosts: ", newPosts)
            #tweeting the posts
            for newPost in newPosts:
                print("newPost: ", newPost)
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
                        link = post.find_element(By.TAG_NAME, "img").get_attribute("src")
                        links = links + link

                    for link in links:
                        urllib.request.urlretrieve(link, str(i)+ ".png")
                        len=len+1
                    
                    try:
                        caption = multipost.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span").text
                        if re.findall("@", caption):
                            biotemp = caption.split("@")
                            caption = biotemp[0] + "@/" + biotemp[1]
                    except:
                        caption=""   
                
                username = multipost.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div[1]/span/a").text
                tweet = "[Instagram Update - " + str(strftime("%d%m%y")) + " " + username + "] (" + link + ")" + "\n\n" + " " + caption + "\n\n#LE_SSERAFIM #르세라핌 #IMFEARLESS"

                files = ""

                if len == 1:
                    api.update_status_with_media(status=tweet, filename="1.png")
                elif len <= 4:
                    for i in range(1, len+1):
                        files = files + (str(i) + ".png")
                        api.update_status_with_media(status=tweet, filename=files)
                elif len <= 8:
                    for i in range(1, 5):
                        files = files + (str(i) + ".png")
                        api.update_status_with_media(status=tweet, filename=files)
                    for i in range(5, len+1):
                        files = files + (str(i) + ".png")
                        status_list = api.user_timeline(user_id=credentials.RECIPIENT_ID)
                        status = status_list[0]
                        json_str = status._json
                        tweetid = json_str["id"]
                        api.update_status_with_media(status=tweet, filename=files, in_reply_to_status_id=tweetid)
                else:
                    for i in range(1, 5):
                        files = files + (str(i) + ".png")
                        api.update_status_with_media(status=tweet, filename=files)
                    for i in range(5, 9):
                        files = files + (str(i) + ".png")
                        status_list = api.user_timeline(user_id=credentials.RECIPIENT_ID)
                        status = status_list[0]
                        json_str = status._json
                        tweetid = json_str["id"]
                        api.update_status_with_media(status=tweet, filename=files, in_reply_to_status_id=tweetid)
                    for i in range(9, len+1):
                        files = files + (str(i) + ".png")
                        status_list = api.user_timeline(user_id=credentials.RECIPIENT_ID)
                        status = status_list[0]
                        json_str = status._json
                        tweetid = json_str["id"]
                        api.update_status_with_media(status=tweet, filename=files, in_reply_to_status_id=tweetid)

                for i in range(1, len+1):
                    os.remove(str(i) + ".png")
                
                #posting the new link to the json file for the next run
                with open('data.json', 'w') as outfile:
                    data = { ["instagramLink" + str(i)]: newPosts[0] }
                    json.dump(data, outfile)    

# tiktok()
instagram()

# if int(strftime("%M"))%10 == 0: