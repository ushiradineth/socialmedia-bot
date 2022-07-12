from pkg import *

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
            dl.urlretrieve(videolink, 'tiktok.mp4')

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