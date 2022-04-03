#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
from datetime import timedelta
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

################################################################################################################
#########################################     Input Variables     ##############################################
download_path=r'C:\Users\Ray\S_Hoc\V1_game_min'
extension_path=r'C:\Users\Ray\S_Hoc\extension_1_19_6_0.crx'

# Seasons to download, can include more seasons by definint season_start and season_end date below
#Positions: S = Skater, G = Goalie

# seasons = ['20072008', '20082009', '20092010', '20102011', '20112012', \
#                         '20122013', '20132014', '20142015', '20152016', '20162017', '20172018']
seasons = ['20182019']
positions = ['S', 'G']

################################################################################################################
################################################################################################################


chrome_options = Options()
chrome_options.add_extension(extension_path)
prefs = {"download.default_directory" : download_path, 'profile.managed_default_content_settings.images':2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path = './chromedriver', options=chrome_options)


for season in seasons:
    if season == '20072008':
#         season_start = datetime(2007, 9, 29)
        season_start = datetime(2007, 11, 17)
        
        season_end = datetime(2008, 4, 6)
    elif season == '20082009':
        season_start = datetime(2008, 10, 4)
        season_end = datetime(2009, 4, 12)
    elif season == '20092010':
        season_start = datetime(2009, 10, 1)
        season_end = datetime(2010, 4, 11)
    elif season == '20102011':
        season_start = datetime(2010, 10, 7)
        season_end = datetime(2011, 4, 10)
    elif season == '20112012':
        season_start = datetime(2011, 10, 6)
        season_end = datetime(2012, 4, 7)
    elif season == '20122013':
        season_start = datetime(2013, 1, 19)
        season_end = datetime(2013, 4, 28)
    elif season == '20132014':
        season_start = datetime(2013, 10, 1)
        season_end = datetime(2014, 4, 13)
    elif season == '20142015':
        season_start = datetime(2014, 10, 8)
        season_end = datetime(2015, 4, 11)
    elif season == '20152016':
        season_start = datetime(2015, 10, 7)
        season_end = datetime(2016, 4, 10)
    elif season == '20162017':
        season_start = datetime(2016, 10, 12)
        season_end = datetime(2017, 4, 9)
    elif season == '20172018':
        season_start = datetime(2017, 10, 4)
        season_end = datetime(2018, 4, 8)
    elif season == '20182019':
        season_start = datetime(2018, 10, 3)
        season_end = datetime(2019, 1, 1)
        
    next_date = season_start - timedelta(days=1)

    while next_date <= season_end:
        next_date = next_date + timedelta(days=1)
        year = str(next_date.year)
        month = str(next_date.month).zfill(2)
        day = str(next_date.day).zfill(2)

        for position in positions:    
            link = None   
            while not link:
                try:
                    nat_url = 'https://www.naturalstattrick.com/playerteams.php?fromseason=' + season + '&thruseason=' + season + '&stype=2&sit=all&score=all&stdoi=oi&rate=y&team=ALL&pos=' + position + '&loc=B&toi=0&gpfilt=gpdate&fd=' + year + '-' + month + '-' + day + '&td=' + year + '-' + month + '-' + day + '&tgp=410&lines=multi&draftteam=ALL'
                    
                    driver.get(nat_url)

                    #to click export button
                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0,1000)")

                    wait = WebDriverWait(driver, 20)
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="players_wrapper"]/div[4]/a[4]/span'))).click()

                    link = driver.find_element_by_xpath('//*[@id="players_wrapper"]/div[4]/a[4]/span')

                    #wait 3 seconds before moving file
                    time.sleep(4)

                    for file in os.listdir(download_path):
                        if file.startswith("Player Season Totals"):
                            os.rename(file, 'Daily_' + year + '_' + month + '_' + day + '_' + position + '_' + '.csv')
                            print('Daily_' + year + '_' + month + '_' + day + '_' + position)

                except NoSuchElementException:
                    driver.close()
                    print('ERROR: ' + year + '_' + month + '_' + day + '_' + position)
driver.close()

