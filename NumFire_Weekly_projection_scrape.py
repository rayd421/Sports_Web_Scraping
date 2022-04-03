#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import time
from datetime import datetime
from datetime import timedelta

###################################################################################################################
#########################################        Input Variables       ############################################

#seasons to pull weekly projection data
seasons = ['2014', '2015', '2016', '2017', '2018', '2019']  


###################################################################################################################
###################################################################################################################

pitcher_table_xpath = '//*[@id="stat-table"]'

team_dict={'ARI':'Diamondbacks', 'ATL':'Braves', 'BAL':'Orioles', 'BOS':'Red Sox', 'CHW':'White Sox', 'CHC':'Cubs',
          'CIN':'Reds', 'CLE':'Indians', 'COL':'Rockies', 'DET':'Tigers', 'MIA':'Marlins', 'HOU':'Astros', 
          'KC':'Royals', 'LAA':'Angels', 'LAD':'Dodgers', 'MIL':'Brewers', 'MIN':'Twins', 'NYM':'Mets',
          'NYY':'Yankees', 'OAK':'Athletics', 'PHI':'Phillies', 'PIT':'Pirates', 'SD':'Padres', 'SF':'Giants',
          'SEA':'Mariners', 'STL':'Cardinals', 'TB':'Rays', 'TEX':'Rangers', 'TOR':'Blue Jays', 'WSH':'Nationals'}

        
for season in seasons:
    if season == '2014':
        season_start = datetime(2014, 3, 24)
        season_end = datetime(2014, 9, 28)
    elif season == '2015':
        season_start = datetime(2015, 3, 30)
        season_end = datetime(2015, 10, 4)
    elif season == '2016':
        season_start = datetime(2016, 3, 28)
        season_end = datetime(2016, 10, 2)
    elif season == '2017':
        season_start = datetime(2017, 3, 27)
        season_end = datetime(2017, 10, 1)
    elif season == '2018':
        season_start = datetime(2018, 3, 26)
        season_end = datetime(2018, 10, 1)
    elif season == '2019':
        season_start = datetime(2019, 3, 18)
        season_end = datetime(2019, 9, 29)
    
    next_date = season_start - timedelta(days=7)
#     next_date = datetime(2019, 7, 13)
    
    while next_date <= season_end:
        next_date = next_date + timedelta(days=7)
        year = str(next_date.year)
        month = str(next_date.month).zfill(2)
        day = str(next_date.day).zfill(2)

        url = 'https://www.numberfire.com/mlb/fantasy/weekly-projections?d='+year+'-'+month+'-'+day
        time.sleep(1)    
        try:
            table= pd.read_html(url)
            time.sleep(1)
        except:
            print('Cant read html {}_{}_{}'.format(year, month, day))
        
        pit_types=[]
        teams=[]
        names=[]
        player_list = [x for x in table[0]['Player']]
        
        for x in player_list:
            line=x.split()

            teams.append(team_dict[line[-1].replace(')','')])
            pit_types.append(line[-2].replace('(','').replace(',', ''))

            name_length= (len(line)-2)/2

            if name_length==1:
                names.append(line[0])
            elif name_length==2:
                names.append(line[0]+' '+line[1])
            elif name_length==3:
                names.append(line[0]+' '+line[1]+' '+line[2])
            elif name_length==4:
                names.append(line[0]+' '+line[1]+' '+line[2]+' '+line[3])
            elif name_length==5:
                names.append(line[0]+' '+line[1]+' '+line[2]+' '+line[3]+' '+line[4])
            elif name_length==2.5:
                names.append(line[0]+' '+line[1]+' '+line[2])
            else:
                print('name length issue length {}'.format(name_length))


            player_df = pd.DataFrame(data={'Name':names, 'Pitcher_type':pit_types, 'Team':teams})

            DF=pd.concat([player_df, table[1]], axis=1)

            DF.to_csv('NF_pit_weekly_{}_{}_{}.csv'.format(year, month, day))

