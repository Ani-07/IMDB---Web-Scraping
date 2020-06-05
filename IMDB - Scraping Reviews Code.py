# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 12:33:17 2020

@author: Anirudh Raghavan
"""

#Source: https://www.dataquest.io/blog/web-scraping-beautifulsoup/

# Scraping username


# Scraping user reviews

# Write a function to pull ratings given a set of usernames

# def ratings_scraper (userprofile_links, usernames):
    
    userratings_db = pd.read_csv("userratings_db.csv") 
    
    #for profile in userprofile_links:
    #    if usernames[userprofile_links.index(profile) in userratings_db[]]:
    #        user1 = profile # Assign url

       # Add Column for user rating
       user_name = userprofile_db['Name'][10]
       userratings_db[user_name] = np.nan
        
       #Get url and convert to bs4
       user1 = userprofile_db["Profile Link"][10]
        
       if requests.get(user1+'/ratings').status_code == 200:
           page_url = user1 + '/ratings'
           response_user1 = requests.get(user1+'/ratings') 
           html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')
           print(200)
            
       elif requests.get(user1+'/reviews').status_code == 200:
           page_url = user1 + '/reviews'
           response_user1 = requests.get(user1+'/reviews') 
           html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')
           print(300)
            
       else:
            print(400)
                               
            #Identify total number of ratings

            n = html_soup_user1.find('div', class_ = 'header').span.text
            n = int(n.replace(',', ''))

            # Identify number of pages to be scraped

            if n%100 == 0:
                pages = n/100
            else:
                pages = n//100+1

            for page in range(pages):
                #Get url and convert to bs4
                response_user1 = requests.get(page_url)
                html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')

                # Scrape movie name and rating
                movie_containers = html_soup_user1.find_all('div', class_ = 'lister-item mode-detail')
                
                for movie in movie_containers:
                    
                    link = 'https://www.imdb.com' + movie.h3.a.get('href')
                    first_div = movie.find('div',class_ = "ipl-rating-star ipl-rating-star--other-user small")
                    
                    rating = first_div.find('span', class_ = "ipl-rating-star__rating").text
                
                    if rating is None:
                        rating = np.nan
                    
                    if link in list(userratings_db['Movie Link']):
                        
                        mov_ind = list(userratings_db['Movie Link']).index(link)
                        
                        userratings_db.loc[mov_ind,user_name] = rating
                         
                    else:
                        name = movie.h3.a.text
                        
                        userratings_db = userratings_db.append({'Movie Name' : name, 
                                            'Movie Link' : link,
                                            user_name : rating}, ignore_index=True)
                        
                # Identify the url of next page
                print(page)
                if page < pages-1:
                    page_url = 'https://www.imdb.com' + html_soup_user1.find('a', class_ = 'flat-button lister-page-next next-page').get('href')
                    
            
            
            #Identify total number of reviews

            n = html_soup_user1.find('div', class_ = 'header').span.text
            n = int(n.split()[0].replace(',',''))

            # Identify number of pages to be scraped

            if n%100 == 0:
                pages = n/100
            else:
                pages = n//100+1

            for page in range(pages):
                #Get url and convert to bs4
                response_user1 = requests.get(page_url)
                html_soup_user1 = BeautifulSoup(response_user1.text, 'html.parser')


                # Scrape movie name and rating
                movie_containers = html_soup_user1.find_all('div', class_ = "review-container")
                
                for movie in movie_containers:
                    
                    link = 'https://www.imdb.com' + movie.a.get('href')
                    rating = movie.find('span',class_ = "rating-other-user-rating")
                    
                    if rating is None:
                        rating = np.nan
                    
                    else:
                        rating = rating.span.text
                                        
                    if link in list(userratings_db['Movie Link']):
                        
                        mov_ind = list(userratings_db['Movie Link']).index(link)
                        
                        userratings_db.loc[mov_ind,user_name] = rating
                         
                    else:
                        name = movie.find('div', class_ = "lister-item-header").a.text
                        
                        userratings_db = userratings_db.append({'Movie Name' : name, 
                                            'Movie Link' : link,
                                            user_name : rating}, ignore_index=True)
                        
                # Identify the url of next page
                print(page)
                if page < pages-1:
                    page_url = 'https://www.imdb.com' + html_soup_user1.find('a', class_ = 'flat-button lister-page-next next-page').get('href')

    
    userratings_db_db.to_csv('userratings_db.csv', index = False)


