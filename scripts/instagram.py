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
        pkg.driver.get("https://www.instagram.com/_zyozyo/")

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
            #tweeting the posts
            for newPost in newPosts:
                pkg.driver.get(newPost)
                caption=""
                len=0

                #single post
                try:
                    singlepost = pkg.WebDriverWait(pkg.driver, 10).until(pkg.EC.presence_of_element_located((pkg.By.CLASS_NAME, "_aato")))
                    link = singlepost.find_element(pkg.By.CSS_SELECTOR, "img").get_attribute("src")
                    pkg.download(link, "1", "png")

                    #single post caption
                    try:
                        caption = singlepost.find_element(pkg.By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span").text
                        if pkg.re.findall("@", caption):
                            biotemp = caption.split("@")
                            caption = biotemp[0] + "@/" + biotemp[1]
                    except Exception as e:
                        print("single post caption error: ", e)
                        caption=""     

                except Exception as e:
                    print("single post error: ", e)

                    #multipost
                    multipost = pkg.WebDriverWait(pkg.driver, 10).until(pkg.EC.presence_of_element_located((pkg.By.CLASS_NAME, "_acay"))) 

                    links = []
                    videoposterlinks = []
                    y = 1

                    try:
                        for i in range(1, 11):
                            try:
                                linkpoint = multipost.find_elements(pkg.By.CSS_SELECTOR, "img")
                                for link in linkpoint:
                                    if link.get_attribute("class") == "_ab1e":
                                        if link.get_attribute("src") not in videoposterlinks:
                                            templink = link.get_attribute("src")
                                            videoposterlinks.append(str(templink))
                                            vlink = str(templink).split("&")[4].split("=")[1]
                                            pkg.download_video(str(vlink), y)
                                            y+=1
                                            pkg.driver.find_element(pkg.By.CLASS_NAME, "_aahi").click()
                                            
                                    else:
                                        if link.get_attribute("src") not in links:
                                            pkg.download(link.get_attribute("src"), str(y), 'png')
                                            y+=1
                                            links.append(link.get_attribute("src"))
                                            pkg.driver.find_element(pkg.By.CLASS_NAME, "_aahi").click()
                            except:
                                pass
                            
                            i+=1

                    except Exception as e:
                        print("multipost error: ", e)

                        #multipost caption                                      
                        try:
                            caption = multipost.find_element(pkg.By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span").text
                            if pkg.re.findall("@", caption):
                                biotemp = caption.split("@")
                                caption = biotemp[0] + "@/" + biotemp[1]
                        except Exception as e:
                            print("multipost caption error: ", e)
                            caption=""  

                    #video
                    # except Exception as e:
                    #     print("video error: ", e)
                    #     video = pkg.WebDriverWait(pkg.driver, 10).until(pkg.EC.presence_of_element_located((pkg.By.CLASS_NAME, "_ab1c")))
                    #     link = video.find_element(pkg.By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div/div/video").get_attribute("src")
                    #     pkg.download(link, "1", "mp4")
                
                tweet = "[Instagram Update - " + str(pkg.strftime("%d%m%y")) + "] (" + newPost + ")" + "\n\n" + caption.strip() + "\n\n#aespa #에스파"

                print(tweet)

                # files = []

                # if len == 1:
                #     pkg.update_status(1, 1, tweet, files)

                # elif len <= 4:
                #     pkg.update_status(1, len+1, tweet, files)

                # elif len <= 8:
                #     tweet1 = pkg.update_status(1, 5, tweet, files)
                #     pkg.update_status_thread(5, len+1, tweet, tweet1, files)

                # else:
                #     tweet1 = pkg.update_status(1, 5, tweet)
                #     tweet2 = pkg.update_status_thread(5, 9, tweet, tweet1, files)
                #     pkg.update_status(9, len+1, tweet2, files)

                # for i in range(0, len+1):
                #     try:
                #         pkg.os.remove(str(i) + ".png")
                #     except:
                #         try:
                #             pkg.os.remove(str(i) + ".mp4")
                #         except:
                #             pass
                
                # #posting the new link to the json file for the next run
                # pkg.update_data('instagramLink', newPost)