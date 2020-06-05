# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 21:45:32 2020

@author: Anirudh Raghavan
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Creating User IDs

user_db = pd.DataFrame(columns = ('Index','Link','Type','Count'))

ids = range(119000000)

119000000/1000000

url = 'https://www.imdb.com/user/ur'

ids2 = [url+str(id) if len(str(id)) > 7 else url+'0'*(7-len(str(id))) + str(id) for id in ids]

start = 0
shift = 999999

for i in range(118):
    locat = r"C:\Users\Anirudh Raghavan\Desktop\Ani\Users\Users_list" + str(119)
    file1 = open(locat,"a")
    for i in ids2[start:start+shift]:
        name = i + "\n" 
        file1.write(name)
    start += shift
    file1.close()    



k = 1
users = open("Users_list1","r")
users = users.read()
users = users.split("\n")
users.pop(-1)


user_db = pd.DataFrame(columns = ('Index', 'link', 'Type','Count'))

n = 0
for id in users:
    if requests.get(id+'/ratings').status_code == 200:
        page_url = id + '/ratings'
        response_user1 = requests.get(id+'/ratings') 
        html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')
        n = html_soup_user1.find('div', class_ = 'header').span.text
        n = int(n.replace(',', ''))
        
        user_db = user_db.append({'Index' : user_db.shape[0] + 1, 
                                            'Link' : id,
                                            'Type' : 'Ratings',
                                            'Count': n}, ignore_index=True)


        print(200)
            
    elif requests.get(id+'/reviews').status_code == 200:
        page_url = id + '/reviews'
        response_user1 = requests.get(id+'/reviews') 
        html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')
        n = html_soup_user1.find('div', class_ = 'header').span.text
        n = int(n.split()[0].replace(',',''))
        
        user_db = user_db.append({'Index' : user_db.shape[0] + 1, 
                                            'Link' : id,
                                            'Type' : 'Reviews',
                                            'Count': n}, ignore_index=True)

        print(300)
            
    else:
        
        user_db = user_db.append({'Index' : user_db.shape[0] + 1, 
                                            'Link' : id,
                                            'Type' : 'None',
                                            'Count': 0}, ignore_index=True)

        print(400)
    n += 1
    print(n)                           
   
name_csv = 'user_db' + k + '.csv'

user_db.to_csv(name_csv, index = False)       