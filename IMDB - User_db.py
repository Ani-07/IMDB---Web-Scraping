# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 21:45:32 2020

@author: Anirudh Raghavan
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from random import sample 
from time import time, sleep


#def IMDB_user(event, context):

def IMDB_user():
    
    # Rate Limits
    max_time = 750
    max_count = 50
    
    
    # First Check Last Link Scraped - File name and link number
    user_log = pd.read_csv("user_log.csv", index_col = False)
    
    if user_log.shape[0] == 0:
        file = 1
        link = 0
    else:
        file = list(user_log['File'])[-1]
        link = list(user_log['Link'])[-1]
    # Open Database required
        
    user_db = pd.read_csv("user_db.csv", index_col = False)
    
    start_time = time()
    elapsed_time = 0
    count = 0
    
    while count <= max_count:
        
        # Based on that open file
    
        file_name = 'Users_list' + str(file)
        users = open(file_name,"r")
        users = users.read()
        users = users.split("\n")
        users.pop(-1)
        
        
        for user in users[link:]:
            
            count += 1
        
            user_ind = users.index(user)
            if requests.get(user+'/ratings').status_code == 200:
                page_url = user + '/ratings'
                response_user1 = requests.get(page_url) 
                html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')
                
                
                try:
                    n = html_soup_user1.find('div', class_ = 'header filmosearch').span.text
                    n = int(n.replace(',', ''))
                except Exception as e: 
                    print(e)
                    n = 0
                
                signal = 'Ratings'
                
                user_db = user_db.append({'Index' : user_db.shape[0] + 1, 
                                                    'Link' : page_url,
                                                    'Type' : signal,
                                                    'Count': n}, ignore_index=True)
        
        
            elif requests.get(user+'/reviews').status_code == 200:
                page_url = user + '/reviews'
                response_user1 = requests.get(page_url) 
                html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')
                
                try:
                    n = html_soup_user1.find('div', class_ = 'header').span.text
                    n = int(n.split()[0].replace(',',''))
                except:
                    n = 0
                        
                signal = 'Reviews'
                
                user_db = user_db.append({'Index' : user_db.shape[0] + 1, 
                                                    'Link' : page_url,
                                                    'Type' : signal,
                                                    'Count': n}, ignore_index=True)
        
                    
            else:
                
                signal = 'None'
                
                user_db = user_db.append({'Index' : user_db.shape[0] + 1, 
                                                    'Link' : user,
                                                    'Type' : signal,
                                                    'Count': 0}, ignore_index=True)
            
        
            
            if user == users[-1]:
                file += 1
                link = 0
            
            sleep(sample([4,8],1)[0])
            
            elapsed_time = time() - start_time
            
            print("{} file {} user - {} - {} link".format(file,user_ind, user,signal))
            
            if elapsed_time > max_time or count > max_count:
                break
            
            
        user_db.to_csv("user_db.csv", index = False)
        
        user_log = user_log.append({'File' : file, 
                                    'Link' : user_ind}, ignore_index=True)
        
        user_log.to_csv("user_log.csv", index = False)
        


for i in range(3):
    IMDB_user()
    sleep(1800)



        