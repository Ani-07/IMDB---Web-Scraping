# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 13:41:29 2020

@author: Anirudh Raghavan
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.imdb.com/title/tt0111161/reviews?ref_=tt_ov_rt' # URL to shawshank Redemption User reviews
response = requests.get(url)
print(response.text[1000:1500])

# Pass URL through beautiful soup library

html_soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find users giving reviews to Shawshank Movie

review_containers = html_soup.find_all('div', class_ = 'review-container')
print(type(review_containers))
print(len(review_containers))



userprofile_db  = pd.read_csv("userprofile_db.csv", index_col = False)

for container in review_containers:
    name = container.find('span', class_ = "display-name-link").a.text #username
    
    # IMDB user ids are unique - so we check if username already present in user_db
    
    if name in list(userprofile_db['Name']):
        print(name)
        continue
    
    profile = 'https://www.imdb.com' + container.find('span', class_ = "display-name-link").a.get('href') #link
    
    profile = profile.split('/')
    if profile[-1][0] == '?':
        del profile[-1]
    profile = '/'.join(profile)
    
    userprofile_db = userprofile_db.append({'Index' : userprofile_db.shape[0] + 1, 
                                            'Name' : name,
                                            'Profile Link' : profile}, ignore_index=True)
        
    
userprofile_db.to_csv('userprofile_db.csv', index = False)
