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
from datetime import datetime, timedelta


########################################################################################################
####################################   Input Variables   ###############################################

extension_path='./extension_1_19_6_0.crx'
seasons_to_download = ['2017', '2018', '2019']

########################################################################################################
########################################################################################################


skater_table_xpath = '//*[@id="stat-table"]'
G_tab_xpath = '/html/body/div[3]/div[2]/div[2]/div/ul/li[5]/a'
G_table_xpath = '//*[@id="stat-table"]/tbody'

chrome_options = Options()
chrome_options.add_extension(extension_path)
driver = webdriver.Chrome(executable_path = './chromedriver', options=chrome_options)      
  
    
for season in seasons:
    if season == '2017':
        season_start = datetime(2017, 10, 4)
        season_end = datetime(2018, 4, 8)
    elif season == '2018':
        season_start = datetime(2018, 10, 3)
        season_end = datetime(2019, 4, 6)
    elif season == '2019':
        season_start = datetime(2019, 10, 2)
        season_end = datetime(2020, 3, 11)
        
    
    next_date = season_start - timedelta(days=1)
    
    while next_date <= season_end:
        next_date = next_date + timedelta(days=1)
        year = str(next_date.year)
        month = str(next_date.month).zfill(2)
        day = str(next_date.day).zfill(2)
        

        url = 'https://swishanalytics.com/optimus/nhl/daily-fantasy-projections?date=' + year + '-' + month + '-' + day

        try:
            driver.get(url)
            #wait for path to be visible and then click
            time.sleep(3)

            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.XPATH, skater_table_xpath)))

            table = driver.find_element_by_xpath(skater_table_xpath)
            time.sleep(2)

            player_names=[]
            player_stats = []
            player_position =[]
            opponent = []

            for ind, player in enumerate(table.text.split('\n')):
                line =player.split()
                if 'vs.' in line:
                    id_ind = line.index('vs.')
                elif '@' in line:
                    id_ind = line.index('@')

                player_position.append(line[id_ind-1])
                opponent.append(line[id_ind+1])
                player_stats.append(line[id_ind+2:])
                player_name_list = (line[:id_ind-1])
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
                                    'Min':[i[0] for i in player_stats], 'SOG':[i[1] for i in player_stats],
                                    'G':[i[2] for i in player_stats], 'A':[i[3] for i in player_stats],
                                    'PPP':[i[4] for i in player_stats], '+/-':[i[5] for i in player_stats],
                                    'BS':[i[6] for i in player_stats], 'Value':[i[7] for i in player_stats],
                                    'Proj Pts':[i[8] for i in player_stats], 'Act Pts':[i[9] for i in player_stats]
                                  })



            skater_df.to_csv('Swish_skater_proj_{}_{}_{}.csv'.format(year, month, day))
            print('saved Swish_skater_proj_{}_{}_{}.csv'.format(year, month, day))
            
        except:
            print('Error Swish_skater_proj_{}_{}_{}.csv'.format(year, month, day))

                
                
        try:    
            wait.until(EC.element_to_be_clickable((By.XPATH, G_tab_xpath))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, G_table_xpath)))
            table2 = driver.find_element_by_xpath(G_table_xpath)
            time.sleep(2)

            goalie_names=[]
            goalie_stats = []
            goalie_position =[]
            goalie_opponent = []

            for ind, goalie in enumerate(table2.text.split('\n')):
                line =goalie.split()
                if 'vs.' in line:
                    id_ind = line.index('vs.')
                elif '@' in line:
                    id_ind = line.index('@')

                goalie_position.append(line[id_ind-1])
                goalie_opponent.append(line[id_ind+1])
                goalie_stats.append(line[id_ind+2:])
                goalie_name_list = (line[:id_ind-1])
                if len(goalie_name_list) == 2:
                    goalie_names.append(goalie_name_list[0] + ' ' + goalie_name_list[1])
                elif len(player_name_list) == 3:
                    goalie_names.append(goalie_name_list[0] + ' ' + goalie_name_list[1] + ' ' + goalie_name_list[2]) 
                elif len(goalie_name_list) == 1:
                    goalie_names.append(player_name_list[0])
                elif len(goalie_name_list) == 4: 
                    goalie_names.append(goalie_name_list[0] + ' ' + goalie_name_list[1] + ' ' + goalie_name_list[2] + ' ' + goalie_name_list[3])
                else:
                    print('Goalie name length issue when parsing from swish')


                goalie_df = pd.DataFrame({'NAME': goalie_names, 'Opponent':goalie_opponent, 
                                    'Min':[i[0] for i in goalie_stats], 'W':[i[1] for i in goalie_stats],
                                    'SO':[i[2] for i in goalie_stats], 'GA':[i[3] for i in goalie_stats],
                                    'SV':[i[4] for i in goalie_stats], 'Value':[i[5] for i in goalie_stats],
                                    'Proj Pts':[i[6] for i in goalie_stats], 'Act Pts':[i[7] for i in goalie_stats]
                                  })


            goalie_df.to_csv('Swish_goalie_proj_{}_{}_{}.csv'.format(year, month, day))
            print('saved Swish_goalie_proj_{}_{}_{}.csv'.format(year, month, day))
            
        except:
            print('Error Swish_goalie_proj_{}_{}_{}.csv'.format(year, month, day))

            
driver.close()

