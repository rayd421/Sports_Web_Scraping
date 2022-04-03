#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
from datetime import timedelta


##########################################################################################
################################   Dependent variables  ##################################

# Path to CRX file. This file extends functionality of Google Chrome web browser 
extension_path = './extension_1_19_6_0.crx'

# Path to chromedriver file
chromedriver_path = './chromedriver'

#fantasydata URL, username, and Password
bask_url = 'https://fantasydata.com/nba/fantasy-basketball-projections'
fantasydata_username = '________________'
fantasydata_password = '________________'

#first date to pull projections (date format 'mm/dd/yyyy')
start_date = '10/28/2019'

#last date to pull projections
last_date_of_season = '11/16/2019'

###########################################################################################
###########################################################################################


#date iterator variable
date_new = start_date

close_popup_xpath = '//*[@id="_ss_popup_36d045e2-68e7-4992-8962-254f0898faa2"]/div[2]/p[1]'
login_button_xpath = '/html/body/div[6]/div/div[2]/header/div/div[4]/div[1]/ul/li[5]/div/a'
email_box_xpath = '/html/body/div[7]/div/div[3]/div/div[3]/div/form/div[1]/div[1]/div[1]/input'
pass_box_xpath = '/html/body/div[7]/div/div[3]/div/div[3]/div/form/div[1]/div[1]/div[2]/input'
confirm_login_button_xpath = '/html/body/div[7]/div/div[3]/div/div[3]/div/form/div[2]/button'
nba_tab_xpath = '/html/body/div[7]/div/div[2]/header/div/div[3]/div/ul/li[3]/div[1]/a'
nba_proj_xpath = '/html/body/div[6]/div/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/ul/li[3]/a'
game_button_xpath = '/html/body/div[6]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/section/div[2]/div[1]/div[1]/div[1]/div[1]/ul/li[2]/a'
button_300_xpath = '/html/body/div[6]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/section/div[2]/div[4]/div[2]/div[2]/a[3]'
date_box_xpath = '/html/body/div[6]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/section/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/span/span/input'

chrome_options = Options()
chrome_options.add_extension(extension_path)
driver = webdriver.Chrome(executable_path = chromedriver_path, options=chrome_options)

link = None   
while not link:
    try:
        
        driver.get(bask_url)
        time.sleep(2)

            #wait for path to be visible and then click
        wait = WebDriverWait(driver, 20)
        wait.until(EC.element_to_be_clickable((By.XPATH, close_popup_xpath))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath))).click()

        wait.until(EC.presence_of_element_located((By.XPATH, email_box_xpath)))
        email_box = driver.find_element_by_xpath(email_box_xpath)
        pass_box = driver.find_element_by_xpath(pass_box_xpath)                                
        email_box.send_keys(fantasydata_username)
        pass_box.send_keys(fantasydata_password)
        wait.until(EC.element_to_be_clickable((By.XPATH, confirm_login_button_xpath))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, nba_tab_xpath))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, nba_proj_xpath))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, game_button_xpath))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, button_300_xpath))).click()
        time.sleep(2)
        link = driver.find_element_by_xpath(date_box_xpath)
        

        while date_new <= last_date_of_season:
            try:
                date_new = datetime.strptime(date_new, '%m/%d/%Y')
                date_new = datetime.strftime(date_new, '%m/%d/%Y')

                wait.until(EC.presence_of_element_located((By.XPATH, date_box_xpath)))
                date_box = driver.find_element_by_xpath(date_box_xpath)
                date_box.clear()
                time.sleep(3)
                driver.execute_script("arguments[0].value = '{}';".format(date_new), date_box) 
                time.sleep(1)
                date_box.click()
                date_box.send_keys(u'\ue007')
                time.sleep(3)

                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'stats-grid-container')))        
                table = driver.find_element_by_class_name('stats-grid-container')
                time.sleep(1)
                
                player_names = []
                player_team_stats = []
                player_stats = []
                for ind, line in enumerate(table.text.split('\n')[1:-2]):
                    
                    if len(line)<6:
                        last_stat_index = ind

                    if len(line)<35 and ind>last_stat_index:
                        player_index = ind-last_stat_index
                        last_player_index = ind

                        if player_index % 2 == 1:
                            if line[-1]=='O' or line[-1]=='Q' or line[-1]=='P':
                                line = line[:-2]
                            rk_len=len(line.split(' ')[0])
                            line = line[rk_len:]    
                            player_names.append(line[1:])

                    elif len(line)>=35 and ind>last_player_index:
                        player_team_stats.append([stat for i, stat in enumerate(line.split(' ')) if i<=2])
                        player_stats.append([float(stat) for i, stat in enumerate(line.split(' ')) if i>2])

                df = pd.DataFrame({'Player': player_names, 'Player_Team':[i[0] for i in player_team_stats], 
                                    'POS':[i[1] for i in player_team_stats], 'OPP':[i[2] for i in player_team_stats],
                                    'PTS':[i[0] for i in player_stats], 'REB':[i[1] for i in player_stats],
                                    'AST':[i[2] for i in player_stats], 'BLK':[i[3] for i in player_stats],
                                    'STL':[i[4] for i in player_stats], 'FG%':[i[5] for i in player_stats],
                                    'FT%':[i[6] for i in player_stats], '3P%':[i[7] for i in player_stats],
                                    'FTM':[i[8] for i in player_stats], '2PM':[i[9] for i in player_stats],
                                    '3PM':[i[10] for i in player_stats], 'TO':[i[11] for i in player_stats],
                                    'Min':[i[12] for i in player_stats], 'FPTS':[i[13] for i in player_stats]
                                  })

                d = datetime.strptime(date_new, '%m/%d/%Y')
                df.to_csv('FanData_proj_{}_{}_{}.csv'.format(d.year, d.month, d.day))
                print('saved FanData_proj_{}_{}_{}.csv'.format(d.year, d.month, d.day))
                date_new = date_new + timedelta(days=1)
                
            except:
                print('Error: {}'.format(date_new))
                date_new = date_new + timedelta(days=1)
            
    except NoSuchElementException:
        time.sleep(2)
        print('Error loading page, retrying.....')
driver.close()


# In[ ]:




