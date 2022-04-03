#!/usr/bin/env python
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import date, datetime
from datetime import timedelta


def get_daily_proj_min():
    
    #Get the roster with correct teams
    rost_url = 'https://www.numberfire.com/nba/players'
    page = requests.get(rost_url)
    lineup_soup = BeautifulSoup(page.content,'html.parser')
    txt_arr = [text for text in lineup_soup.stripped_strings]

    start_index = txt_arr.index('A-Z (Last Name)')
    end_index = txt_arr.index('NBA PLAYER NEWS')
    team_list=[]
    name_list=[]

    for i, x in enumerate(txt_arr):
        if i>start_index and i<end_index:
            if (i-start_index) % 2 == 0:
                team_list.append(x.split()[1][:-1])
            elif (i-start_index) % 2 == 1:
                name_list.append(x)    

    name_list=np.asarray(name_list).reshape(-1,1)
    team_list=np.asarray(team_list).reshape(-1,1)

    roster = np.concatenate((name_list, team_list), axis=1)

    
    #add players who are not on numberfire players list (https://www.numberfire.com/nba/players)
    add_players = np.asarray((['Onyeka Okongwu','ATL'],['Ben Simmons','PHI'], ['Isaiah Jackson','IND'], ['Khris Middleton','MIL'],                              ['Kevin Love','CLE']))

    roster=np.concatenate((roster, add_players))
    
    #Get the projections
    current_date=date.today()
    player_name_list=[]
    home_team_list=[]
    away_team_list=[]
    player_team = []

    nf_url = 'https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections'
    df = pd.read_html(nf_url)

    for ind, x in enumerate(df[3]['Unnamed: 0_level_0']['Player']):
        line=x.split()
        at_index= line.index('@')
        home_team = line[at_index+1]
        away_team = line[at_index-1]
        player_last=line[at_index-3]
        
        name_len=(at_index-3)-line.index(player_last)
        
        if name_len == 2:
            player_name=line[at_index-4]+' '+player_last
        elif name_len == 3:
            player_name=line[at_index-5]+' '+line[at_index-4]+' '+player_last
        elif name_len == 1:
            player_name=player_last
        elif name_len == 0:
            player_name=line[at_index-5]+' '+line[at_index-4]+' '+player_last
        
        
        player_name_list.append(player_name)
        home_team_list.append(home_team)
        away_team_list.append(away_team)
        
    roster_name_list=[x[0] for x in roster]

    
    for player in player_name_list:
        if player not in roster_name_list:
            print('{} not found in roster team list'.format(player))
        else:
            roster_index = roster_name_list.index(player)
            player_team.append(roster[roster_index][1])
            
    if len(player_name_list) != len(set(player_name_list)):
        print('There are duplicate names in projection list')

    df1=pd.DataFrame({'Player':player_name_list, 'Player_Team':player_team, 'Home_Team':home_team_list, 'Away_team':away_team_list})  
    df2=df[3]['Stats']
    df_final=pd.concat([df1, df2], axis=1, sort=False)
    df_final.to_csv('./NumFir_proj_{}_{}_{}.csv'.format(str(current_date.year), str(current_date.month), str(current_date.day)))
    print('Number Fire projections saved to csv')


# In[ ]:




