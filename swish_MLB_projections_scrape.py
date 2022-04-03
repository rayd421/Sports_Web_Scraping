#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


################################################################################################################
######################################         Input Variables       ###########################################

extension_path = '.\extension_1_19_6_0.crx'
chrome_driver_path = './chromedriver.exe'
seasons = ['2019', '2020']

################################################################################################################
################################################################################################################


pitcher_table_xpath = '//*[@id="stat-table"]'
chrome_options = Options()
chrome_options.add_extension(extension_path)
driver = webdriver.Chrome(executable_path = chrome_driver_path, options=chrome_options)


for season in seasons:
    if season == '2010':
        season_start = datetime(2010, 4, 4)
        season_end = datetime(2010, 10, 3)
    elif season == '2011':
        season_start = datetime(2011, 3, 31)
        season_end = datetime(2011, 9, 28)
    elif season == '2012':
        season_start = datetime(2012, 3, 28)
        season_end = datetime(2012, 10, 3)    
    elif season == '2013':
        season_start = datetime(2013, 3, 31)
        season_end = datetime(2013, 9, 29)
    elif season == '2014':
        season_start = datetime(2014, 3, 30)
        season_end = datetime(2014, 9, 28)
    elif season == '2015':
        season_start = datetime(2015, 4, 5)
        season_end = datetime(2015, 10, 4)
    elif season == '2016':
        season_start = datetime(2016, 4, 3)
        season_end = datetime(2016, 10, 2)
    elif season == '2017':
        season_start = datetime(2017, 4, 2)
        season_end = datetime(2017, 10, 1)
    elif season == '2018':
        season_start = datetime(2018, 3, 29)
        season_end = datetime(2018, 10, 1)
    elif season == '2019':
        season_start = datetime(2019, 3, 28)
        season_end = datetime(2019, 3, 29)
    elif season == '2020':
        season_start = datetime(2020, 7, 20)
        season_end = datetime(2020, 7, 22)
    
    
    next_date = season_start - timedelta(days=1)
    
    while next_date <= season_end:
        next_date = next_date + timedelta(days=1)
        year = str(next_date.year)
        month = str(next_date.month).zfill(2)
        day = str(next_date.day).zfill(2)


        url = 'https://swishanalytics.com/optimus/mlb/dfs-batter-projections?date=' + year + '-' + month + '-' + day

        try:
            driver.get(url)
            #wait for path to be visible and then click
            time.sleep(3)

            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.XPATH, pitcher_table_xpath)))

            table = driver.find_element_by_xpath(pitcher_table_xpath)
            time.sleep(2)

            player_names=[]
            player_stats = []
            player_position =[]
            opponent = []

            for ind, player in enumerate(table.text.split('\n')[18:]):
                line =player.split()
                if 'vs' in line:
                    id_ind = line.index('vs')
                elif '@' in line:
                    id_ind = line.index('@')


                opponent.append(line[id_ind+1])
                player_stats.append(line[id_ind+5:id_ind+16])
                player_name_list = (line[:id_ind-2])
                if len(player_name_list) == 2:
                    player_names.append(player_name_list[0] + ' ' + player_name_list[1])
                elif len(player_name_list) == 3:
                    player_names.append(player_name_list[0] + ' ' + player_name_list[1] + ' ' + player_name_list[2]) 
                elif len(player_name_list) == 1:
                    player_names.append(player_name_list[0])
                elif len(player_name_list) == 4: 
                    player_names.append(player_name_list[0] + ' ' + player_name_list[1] + ' ' + player_name_list[2] + ' ' + player_name_list[3])
                else:
                    print('Player name length issue when parsing from swish')


                skater_df = pd.DataFrame({'NAME': player_names, 'Opponent':opponent, 
                                    'AB':[i[0] for i in player_stats], 'BB':[i[1] for i in player_stats],
                                    'HBP':[i[2] for i in player_stats], '1B':[i[3] for i in player_stats],
                                    '2B':[i[4] for i in player_stats], '3B':[i[5] for i in player_stats], 
                                    'HR':[i[6] for i in player_stats], 'RBI':[i[7] for i in player_stats],
                                    'Runs':[i[8] for i in player_stats], 'SB':[i[9] for i in player_stats],
                                    'CS':[i[10] for i in player_stats] 
                                  })


            if len(player_name_list) != len(set(player_name_list)):
                print('There are duplicate names in projection list')

            skater_df.to_csv('Swish_pitcher_proj_{}_{}_{}.csv'.format(year, month, day))
            print('saved Swish_pitcher_proj_{}_{}_{}.csv'.format(year, month, day))

        except:
            print('Error Swish_pitcher_proj_{}_{}_{}.csv'.format(year, month, day))

driver.close()


# In[ ]:




