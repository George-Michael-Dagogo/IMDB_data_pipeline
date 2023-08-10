#url = "https://www.imdb.com/search/title/?title_type=feature&year=2023-01-01,2023-06-18"
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import uuid
from sqlalchemy import create_engine,text
import concurrent.futures


today = datetime.date.today()
url = [f'https://www.imdb.com/search/title/?title_type=feature&year=2023-01-01,{today}&start={i:d}&ref_=adv_nxt'  for i in (range(1, 5394, 50))]

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
            titles.append('No title')


        if box.h3.find('span', class_= 'lister-item-year text-muted unbold') is not None: 
                #year released
            year = box.h3.find('span', class_= 'lister-item-year text-muted unbold').text # remove the parentheses around the year and make it an integer
            years.append(year)
        else:
            years.append('No year')

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
            runtimes.append('No runtime')

        if box.find('div', class_ = 'inline-block ratings-imdb-rating') is not None:
            #IMDB ratings
            imdb = float(box.find('div', class_ = 'inline-block ratings-imdb-rating').text) # non-standardized variable
            imdb_ratings.append(imdb)
        else:
            imdb_ratings.append('No rating')

        if box.find('span', class_ = 'metascore') is not None:
                #Metascore
            m_score = int(box.find('span', class_ = 'metascore').text) # make it an integer
            metascores.append(m_score)
        else:
            metascores.append('No score')

        if box.find('p', class_ = 'sort-num_votes-visible') is not None:
                #Number of votes
            vote = str(box.find('p', class_ = 'sort-num_votes-visible').text)
            numeric_filter = filter(str.isdigit, vote)
            vote = "".join(numeric_filter)
            votes.append(vote)
        else:
            votes.append('No votes')
    print('ended')



def to_database():
    movie_df = pd.DataFrame({'movie': titles, 
                        'year': years,
                        'rating': ratings,
                        'genre': genres,
                        'runtime_min': runtimes,
                        'imdb_rating': imdb_ratings,
                        'metascore': metascores,
                        'votes': votes})
    movie_df['year'] = movie_df['year'].str[-5:-1]
    movie_df.to_csv('movie.csv', index=False)

    try:
        conn_string = 'postgresql://testtech:your_password@testtech.postgres.database.azure.com:5432/postgres'

        db = create_engine(conn_string)
        conn = db.connect()    
        movie_df.to_sql('movies', con=conn, if_exists='append',index=False)
        print('push done')

    finally:
        print('okay')


with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(scraper_per_page, url)
to_database()