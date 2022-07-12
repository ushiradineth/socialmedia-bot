from pkg import *

def instagram():
    # try:
        #login to instagram
        driver.get("https://www.instagram.com/")
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)

            driver.get("https://www.instagram.com/")

        except:
            login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]")))
            username = driver.find_element(By.NAME, "username")
            username.send_keys(credentials.INSTAGRAM_USERNAME)
            password = driver.find_element(By.NAME, "password")
            password.send_keys(credentials.INSTAGRAM_PASSWORD)
            driver.find_element(By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]").click()
            logindone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/div/div/div/section/div/button")))
            pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

        #getting the last tweeted instagram link from the json file
        with open('data.json', 'r') as f:
            data = json.load(f)
            latest_link = (data["instagramLink"])

        #go to the instagram page
        driver.get("https://www.instagram.com/k_a_z_u_h_a__/")

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
        newPosts.reverse()

        if c == True:
            #tweeting the posts
            for newPost in newPosts:
                driver.get(newPost)
                caption=""
                len=0

                #single post
                try:
                    singlepost = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_aato")))
                    link = singlepost.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                    dl.urlretrieve(link, '1.png')

                    #single post caption
                    try:
                        caption = singlepost.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span").text
                        if re.findall("@", caption):
                            biotemp = caption.split("@")
                            caption = biotemp[0] + "@/" + biotemp[1]
                    except Exception as e:
                        print("single post caption error: ", e)
                        caption=""     

                except Exception as e:
                    print("single post error: ", e)

                    #multipost
                    try:
                        multipost = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_acay")))  
                        pics = []
                        try:
                            lastpic = ""
                            for i in range(1, 11):
                                if i != 1:
                                    pics.append(multipost.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div[2]/div/div/div/ul/li[3]/div/div/div/div/div[1]/img").get_attribute("src"))
                                    driver.find_element(By.CLASS_NAME, "_aahi").click()
                                else:
                                    pics.append(multipost.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/img").get_attribute("src"))
                                    driver.find_element(By.CLASS_NAME, "_aahi").click()

                            print(pics)
                                                              
                                    
                        except Exception as e:
                            print("multipost error: ", e)

                        #multipost caption                                      
                        try:
                            caption = multipost.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span").text
                            if re.findall("@", caption):
                                biotemp = caption.split("@")
                                caption = biotemp[0] + "@/" + biotemp[1]
                        except Exception as e:
                            print("multipost caption error: ", e)
                            caption=""  

                    #video
                    except Exception as e:
                        print("video error: ", e)
                        video = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_ab1c")))
                        link = video.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div/div/video").get_attribute("src")
                        dl.urlretrieve(link, '1.mp4')

                tweet = "[Instagram Update - " + str(strftime("%d%m%y")) + "] (" + newPost + ")" + "\n\n" + caption.strip() + "\n\n#aespa #에스파"

                files = []

                if len == 1:
                    try:
                        upload_result = api.media_upload("1.png")
                    except:
                        upload_result = api.media_upload("1.mp4")

                    api.update_status(status=tweet, media_ids=upload_result.media_id_string)
                    upload_result=""

                elif len <= 4:
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

                for i in range(0, len+1):
                    try:
                        os.remove(str(i) + ".png")
                    except:
                        try:
                            os.remove(str(i) + ".mp4")
                        except:
                            pass
                
                #posting the new link to the json file for the next run
                with open('data.json', 'r+') as outfile:
                    data = json.load(outfile)
                    data['instagramLink'] = newPost
                    outfile.seek(0)
                    json.dump(data, outfile, indent=4)
                    outfile.truncate() 