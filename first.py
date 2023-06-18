#url = "https://www.imdb.com/search/title/?title_type=feature&year=2023-01-01,2023-06-18"
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

today = datetime.date.today()
url = [f'https://www.imdb.com/search/title/?title_type=feature&year=2023-01-01,{today}&start={i:d}&ref_=adv_nxt'  for i in (range(1,500, 50))]

titles = []
years = []
ratings = []
genres = []
runtimes = []
imdb_ratings = []
metascores = []
votes = []

def scraper_per_page(url):
    print('began')
    page = requests.get(url)
    soup = BeautifulSoup(page.text,  "html.parser")
    movie_box = soup.find_all('div', class_ = 'lister-item mode-advanced')
    for box in movie_box:

        if box.find('h3', class_ = 'lister-item-header') is not None:
            title = box.find('h3', class_ = 'lister-item-header').a.text
            titles.append(title)
        else:
            titles.append('None')


        if box.h3.find('span', class_= 'lister-item-year text-muted unbold') is not None: 
                #year released
            year = box.h3.find('span', class_= 'lister-item-year text-muted unbold').text # remove the parentheses around the year and make it an integer
            years.append(year)
        else:
            years.append(None)

        if box.p.find('span', class_ = 'certificate') is not None:
            #rating
            rating = box.p.find('span', class_= 'certificate').text
            ratings.append(rating)
        else:
            ratings.append("No rating")

        if box.p.find('span', class_ = 'genre') is not None:  
                #genre
            genre = box.p.find('span', class_ = 'genre').text.replace("\n", "").rstrip().split(',') # remove the whitespace character, strip, and split to create an array of genres
            genres.append(genre)  
        else:
            genres.append("No genre")

        if box.p.find('span', class_ = 'runtime') is not None:
                #runtime
            time = int(box.p.find('span', class_ = 'runtime').text.replace(" min", "")) # remove the minute word from the runtime and make it an integer
            runtimes.append(time)
        else:
            runtimes.append(None)

        if float(box.strong.text) is not None:
            #IMDB ratings
            imdb = float(box.strong.text) # non-standardized variable
            imdb_ratings.append(imdb)
        else:
            imdb_ratings.append(None)

        if box.find('span', class_ = 'metascore') is not None:
                #Metascore
            m_score = int(box.find('span', class_ = 'metascore').text) # make it an integer
            metascores.append(m_score)
        else:
            metascores.append(None)

        if box.find('span', attrs = {'name':'nv'})['data-value'] is not None:
                #Number of votes
            vote = int(box.find('span', attrs = {'name':'nv'})['data-value'])
            votes.append(vote)
        else:
            votes.append(None)
    print('ended')

        

for i in url:
    scraper_per_page(i)

movie_df = pd.DataFrame({'movie': titles, 'year': years,'rating': ratings,'genre': genres,'runtime_min': runtimes,'imdb': imdb_ratings,'metascore': metascores, 'votes': votes}                  )
print(movie_df)
