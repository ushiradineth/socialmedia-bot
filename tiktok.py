from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.tiktok.com/@le_sserafim?lang=en")

div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tiktok-yz6ijl-DivWrapper")))
driver.get(div.find_element_by_css_selector('a').get_attribute('href'))
