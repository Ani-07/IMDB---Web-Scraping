# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 12:33:17 2020

@author: Anirudh Raghavan
"""

#Source: https://www.dataquest.io/blog/web-scraping-beautifulsoup/

# Scraping username

import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://www.imdb.com/title/tt0111161/reviews?ref_=tt_ov_rt'
response = requests.get(url)
print(response.text[1000:1500])


html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)


review_containers = html_soup.find_all('div', class_ = 'review-container')
print(type(review_containers))
print(len(review_containers))


first_review = review_containers[1]

username = []
userrating = []
userprofile = []

for container in review_containers:
    name = container.find('span', class_ = "display-name-link").a.text #username
    username.append(name)
    
    if container.span.span is not None:
        rating = container.span.span.text #rating
        userrating.append(rating)
    else:
        rating = '-' #rating
        userrating.append(rating)
    
    profile = 'https://www.imdb.com' + container.find('span', class_ = "display-name-link").a.get('href') + 'ratings' #link
    userprofile.append(profile)

userprofile_db = pd.DataFrame({'Name': username, 'Profile Link': userprofile})

userprofile_db.head(10)
userprofile_db.to_csv('userprofile_db.csv')


# Scraping user reviews

# Write a function to pull ratings given a set of usernames

def ratings_scraper (userprofile_links, usernames):
    
    userratings_db = pd.read_csv("userratings_db.csv") 
    
    for profile in userprofile_links:
        if usernames[userprofile_links.index(profile) in userratings_db[]]
        user1 = profile # Assign url

        #Get url and convert to bs4
        response_user1 = requests.get(user1)
        if response_user1.status_code == 200:
            html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')

            #Identify total number of reviews

            n = html_soup_user1.find('div', class_ = 'lister-list-length').span.text
            n = int(n.replace(',', ''))

            # Identify number of pages to be scraped

            if n%100 == 0:
                pages = n/100
            else:
                pages = n//100+1

            for page in range(pages):
                #Get url and convert to bs4
                response_user1 = requests.get(user1)
                html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')

                # Scrape movie name and rating
                movie_containers = html_soup_user1.find_all('div', class_ = 'lister-item mode-detail')
                
                for movie in movie_containers:
                    name = movie.h3.a.text
                    movies.append(name)
                    
                    link = 'https://www.imdb.com' + movie.h3.a.get('href')
                    links.append(link)
    
                    rating = movie.find('span',class_ = "ipl-rating-star__rating").text
                    ratings.append(rating)

                # Identify the url of next page
                print(page)
                if page < pages-1:
                    user1 = 'https://www.imdb.com' + html_soup_user1.find('a', class_ = 'flat-button lister-page-next next-page').get('href')
    



