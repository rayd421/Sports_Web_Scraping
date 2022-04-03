#!/usr/bin/env python
# coding: utf-8

# In[5]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta

#####################################################################################################################
##############################################     Input Variables    ###############################################

start_date = datetime(2018, 10, 15)
end_date = datetime(2018, 10, 17)

#####################################################################################################################
#####################################################################################################################


game_date = start_date

while game_date < end_date:
    try:
        url = 'https://rotogrinders.com/lineups/nba?date=' + str(game_date.year) + '-' +                             str(game_date.month) + '-' + str(game_date.day) + '&site=fanduel'

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36                     (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content,'html.parser')

        txt_arr = [text for text in soup.stripped_strings]

        starter_index = [i for i, x in enumerate(txt_arr) if str(x) == 'Starters']
        bench_index = [i for i, x in enumerate(txt_arr) if str(x) == 'Bench']
        schedule_index = [i for i, x in enumerate(txt_arr) if str(x) == 'Edit Schedule']
        away_team_starters = []
        home_team_starters = []
        away_team_bench = []
        home_team_bench = []
        date = []
        home_or_bench = []
        lineup = []
        team=[]


        for i, x in enumerate(starter_index):
            if i%2 == 0:
                if txt_arr[x-1].find('Lineup') != -1:
                    tm_offset=4
                elif txt_arr[x-1].find('Lineup') == -1:
                    tm_offset=0
                home_team_name = txt_arr[x-8-tm_offset]
                away_team_name = txt_arr[x-11-tm_offset]

                for j in range(bench_index[i]-starter_index[i]):
                    if len(txt_arr[starter_index[i]+j+1])>6:
                        away_team_starters.append(txt_arr[starter_index[i]+1+j])
                        lineup.append(txt_arr[starter_index[i]+1+j])
                        team.append(away_team_name)
                        home_or_bench.append('starter')
                        date.append(game_date)


                for k in range(starter_index[i+1]-bench_index[i]-1-tm_offset):
                    if len(txt_arr[bench_index[i]+k+1])>6:
                        away_team_bench.append(txt_arr[bench_index[i]+1+k])
                        lineup.append(txt_arr[bench_index[i]+1+k])
                        team.append(away_team_name)
                        home_or_bench.append('bench')
                        date.append(game_date)

            if i%2 == 1:
                if txt_arr[x-1].find('Lineup') != -1:
                    lin_offset=4
                elif txt_arr[x-1].find('Lineup') == -1:
                    lin_offset=0
                if txt_arr[schedule_index[int(i/2)] - 2] == 'Grind Down':
                    sched_offset = 3
                else:
                    sched_offset = 2

                for j in range(bench_index[i]-starter_index[i]-lin_offset):
                    if len(txt_arr[starter_index[i]+j+1])>6:
                        home_team_starters.append(txt_arr[starter_index[i]+1+j])
                        lineup.append(txt_arr[starter_index[i]+1+j])
                        team.append(home_team_name)
                        home_or_bench.append('starter')
                        date.append(game_date)


                for k in range(schedule_index[int(i/2)]-bench_index[i]-1-sched_offset):
                    if len(txt_arr[bench_index[i]+k+1])>6:
                        home_team_bench.append(txt_arr[bench_index[i]+1+k])
                        lineup.append(txt_arr[bench_index[i]+1+k])
                        team.append(home_team_name)
                        home_or_bench.append('bench')
                        date.append(game_date)


        df = pd.DataFrame({'Date':date, 'Team':team,  'Name':lineup, 'Status':home_or_bench})    

        df.to_csv('Daily_lineup_{}_{}_{}.csv'.format(str(game_date.year), str(game_date.month), str(game_date.day)))

        print('Saved Daily_lineup_{}_{}_{}.csv'.format(str(game_date.year), str(game_date.month), str(game_date.day)))
        game_date = game_date + timedelta(days=1)
        
    except:
        print('Error {}-{}-{}'.format(str(game_date.year), str(game_date.month), str(game_date.day)))
        game_date = game_date + timedelta(days=1)
        


# In[ ]:




