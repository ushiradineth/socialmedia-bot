import pkg
from pkg import *

def tiktok():

    try:
        #getting the last tweeted tiktok link from the json file
        latest_tiktok = pkg.get_data("tiktokLink")

        pkg.driver.get("https://www.tiktok.com/@aespa_official")

        #waits until the page loads
        div = WebDriverWait(pkg.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div")))

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
            try:
                div = WebDriverWait(pkg.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div")))
                link = div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[1]/div/div/a").get_attribute("href")
                bio = div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[2]/a").get_attribute("title")
                
                if bio != "":
                    bio = "\n\n" + str(bio)
                    
                    #fixing hashtags
                    biotext = bio.split("#")

                    if re.findall('with', bio):
                        biotext[0] = biotext[0].replace("with", "")
                        
                    biotext[0] = biotext[0].replace("@", "@/")

                    hashtaglist = "#KARINA", "#카리나", "#GISELLE", "#지젤", "#WINTER", "#윈터", "#NINGNING", "#닝닝"
                    hashtags = ""
                    for hashtag in hashtaglist:
                        if re.findall(hashtag, bio):
                            hashtags = hashtags + " " + hashtag
                
                #downloading the video
                pkg.driver.get(div.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[" + str(i) + "]/div[1]/div/div/a").get_attribute("href"))
                div1 = WebDriverWait(pkg.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[1]/div[2]/div/div/div")))
                videolink = div1.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div[1]/div[2]/div/div/div/video").get_attribute("src")
                pkg.download(videolink, "tiktok", "mp4")

                #tweeting
                tweet = "[TikTok Update - " + str(strftime("%d%m%y")) + "] (" + link + ")" + " ".join(biotext[0].strip().split()) + "\n\n#aespa #에스파" + hashtags
                upload_result = pkg.api.media_upload('downloads\\tiktok.mp4')
                pkg.api.update_status(status=tweet, media_ids=[upload_result.media_id_string])
                os.remove('downloads\\tiktok.mp4')
                upload_result=""
                
                #posting the new link to the json file for the next run
                if i == 1:
                    pkg.update_data('tiktokLink', link)
                
                pkg.driver.get("https://www.tiktok.com/@aespa_official")
            except Exception as e:
                pkg.errorDM("tiktok", e)
    
    except Exception as e:
        pkg.errorDM("tiktok", e)