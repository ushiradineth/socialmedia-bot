import pkg
from pkg import *


def instagram():
    # try:
        #login to instagram
        pkg.driver.get("https://www.instagram.com/")

        pkg.instagram_login()

        #getting the last tweeted instagram link from the json file
        latest_link = pkg.get_data("instagramLink")

        #go to the instagram page
        pkg.driver.get("https://www.instagram.com/aespa_official/")

        #waits until the page loads
        instagramPage = pkg.WebDriverWait(pkg.driver, 10).until(pkg.EC.presence_of_element_located((pkg.By.CLASS_NAME, "_aa-i")))
        postRows = instagramPage.find_elements(pkg.By.CLASS_NAME, "_ac7v")
        newPosts=[]

        c=False

        #getting the new posts
        for postRow in postRows:
            posts = postRow.find_elements(pkg.By.CLASS_NAME, "_aabd")
            for post in posts:
                link = post.find_element(pkg.By.TAG_NAME, "a").get_attribute("href")
                if (link==latest_link):
                    break
                newPosts.append(link)
                c=True
            else:
                continue
            break
        newPosts.reverse()

        if c == True:

            #getting and tweeting the posts
            for newPost in newPosts:
                pkg.driver.get(newPost)
                caption = ""
                lenn = 0

                #single post
                try:
                    singlepost = pkg.WebDriverWait(pkg.driver, 10).until(pkg.EC.presence_of_element_located((pkg.By.CLASS_NAME, "_aato")))

                    #img
                    try:
                        link = singlepost.find_element(pkg.By.CSS_SELECTOR, "img").get_attribute("src")
                        pkg.download(link, "1", "png")
                        lenn = 1
                        #single post caption
                        try:
                            caption = "\n\n" + singlepost.find_element(pkg.By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]").text.replace("#", "#/").replace("@", "@/")
                            caption = caption[:190] + '..' * (len(caption) > 190)

                        except Exception as e:
                            if "Stacktrace:" not in str(e):
                                print("single img caption error: ", e)
                            caption=""   

                    #reel    
                    except:
                        links = []
                        videoposterlinks = []

                        try:
                            linkclass = singlepost.find_element(pkg.By.CSS_SELECTOR, "video").get_attribute("class")
                            if linkclass == "_ab1d":
                                if singlepost.find_element(pkg.By.CSS_SELECTOR, "video").get_attribute("poster") not in videoposterlinks:
                                    templink = singlepost.find_element(pkg.By.CSS_SELECTOR, "video").get_attribute("poster")
                                    videoposterlinks.append(str(templink))
                                    lenn+=1
                                    vlink = str(templink).split("&")[4].split("=")[1]
                                    pkg.download_video(str(vlink), lenn)

                        except Exception as e:
                            if "Stacktrace:" not in str(e):
                                print("single post error: ", e)

                        #reel caption
                        try:
                            caption = "\n\n" + singlepost.find_element(pkg.By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]").text.replace("#", "#/").replace("@", "@/")[:190] + '..' * (len(caption) > 190)
                            
                        except Exception as e:
                            if "Stacktrace:" not in str(e):
                                print("reel caption error: ", e)
                            caption=""   

                except Exception as e:
                    if "Stacktrace:" not in str(e):
                        print("single post error: ", e)
                    
                    #multipost
                    try:                   
                        multipost = pkg.WebDriverWait(pkg.driver, 10).until(pkg.EC.presence_of_element_located((pkg.By.CLASS_NAME, "_acay"))) 

                        links = []
                        videoposterlinks = []
                        y = 0

                        for i in range(1, 11):
                            try:
                                linkpoint = multipost.find_elements(pkg.By.CSS_SELECTOR, "img")
                                for link in linkpoint:
                                    if link.get_attribute("class") == "_ab1e":
                                        if link.get_attribute("src") not in videoposterlinks:
                                            templink = link.get_attribute("src")
                                            videoposterlinks.append(str(templink))
                                            y+=1
                                            vlink = str(templink).split("&")[4].split("=")[1]
                                            pkg.download_video(str(vlink), y)
                                            pkg.driver.find_element(pkg.By.CLASS_NAME, "_aahi").click()
                                            
                                    else:
                                        if link.get_attribute("src") not in links:
                                            y+=1
                                            pkg.download(link.get_attribute("src"), str(y), 'png')
                                            links.append(link.get_attribute("src"))
                                            pkg.driver.find_element(pkg.By.CLASS_NAME, "_aahi").click()
                            except:
                                pass
                            
                            i+=1
                        
                        lenn = y

                        # multipost caption    
                        try:
                            caption = "\n\n" + multipost.find_element(pkg.By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]").text.replace("#", "#/").replace("@", "@/")
                            caption = caption[:190] + '..' * (len(caption) > 190)

                        except Exception as e:
                            if "Stacktrace:" not in str(e):
                                print("multipost caption error: ", e)
                            caption=""  

                    except Exception as e:
                        if "Stacktrace:" not in str(e):
                            print("multipost error: ", e)

                        try:
                            # video
                            video = pkg.WebDriverWait(pkg.driver, 10).until(pkg.EC.presence_of_element_located((pkg.By.CLASS_NAME, "_ab1c")))
                            link = video.find_element(pkg.By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div/div/video").get_attribute("src")
                            pkg.download(link, "1", "mp4")
                            lenn = 1
                        
                        except Exception as e:
                            if "Stacktrace:" not in str(e):
                                print("video error: ", e)


                try:   
                    tweet = "[Instagram Update - " + str(pkg.strftime("%d%m%y")) + "] (" + newPost + ")" + str(caption) + "\n\n#aespa #에스파"
                    tweet = tweet[:280] + '..' * (len(caption) > 280)
                    print(tweet) 
                    

                    pkg.update_status(tweet, lenn)

                    # for i in range(1, lenn+1):
                    #     try:
                    #         pkg.os.remove("downloads\\" + str(i) + ".png")
                    #     except:
                    #         try:
                    #             pkg.os.remove("downloads\\" + str(i) + ".mp4")
                    #         except:
                    #             pass
                    
                    # #posting the new link to the json file for the next run
                    # pkg.update_data('instagramLink', newPost)
                except Exception as e:
                    print("end error: ", e)