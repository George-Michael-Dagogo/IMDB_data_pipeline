from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import psycopg2
from sqlalchemy import create_engine

today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=1)
url = 'https://www.imdb.com/search/title/?title_type=feature&year='+ str(yesterday) +','+ str(today) +'&start=1&ref_=adv_nxt'

titles = []
years = []
ratings = []
genres = []
runtimes = []
imdb_ratings = []
metascores = []
votes = []

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

    if box.find('div', class_ = 'inline-block ratings-imdb-rating') is not None:
        #IMDB ratings
        imdb = float(box.find('div', class_ = 'inline-block ratings-imdb-rating').text) # non-standardized variable
        imdb_ratings.append(imdb)
    else:
        imdb_ratings.append(None)

    if box.find('span', class_ = 'metascore') is not None:
            #Metascore
        m_score = int(box.find('span', class_ = 'metascore').text) # make it an integer
        metascores.append(m_score)
    else:
        metascores.append(None)

    if box.find('p', class_ = 'sort-num_votes-visible') is not None:
            #Number of votes
        vote = int(box.find('p', class_ = 'sort-num_votes-visible').text.replace('\n','').replace('Votes:','').replace(',',''))
        votes.append(vote)
    else:
        votes.append(None)
print('ended')

        

movie_df = pd.DataFrame({'movie': titles, 
                        'year': years,
                        'rating': ratings,
                        'genre': genres,
                        'runtime_min': runtimes,
                        'imdb': imdb_ratings,
                        'metascore': metascores,
                        'votes': votes})
movie_df['year'] = movie_df['year'].str[-5:-1] 

print(movie_df)


conn_string = 'postgresql://testtech:2@testtech.postgres.database.azure.com:5432/postgres'

db = create_engine(conn_string)
conn = db.connect()

#movie_df.to_sql('imdb_movies', con=conn, if_exists='append',index=False)
conn.close()

conn = psycopg2.connect(database='postgres',
                                user='testtech', 
                                password='',
                                host='testtech.postgres.database.azure.com'
        )



conn.autocommit = True
cursor = conn.cursor()
sql2 = '''DELETE FROM imdb_movies T1 USING imdb_movies T2 
    WHERE T1.ctid < T2.ctid 
    AND  T1.movie = T2.movie;'''
    #The “CTID” field is a field that exists in every PostgresSQL table, 
    #it is always unique for each and every record in the table
cursor.execute(sql2)

sql3 = '''SELECT COUNT(*) FROM imdb_movies;'''
cursor.execute(sql3)
for q in cursor.fetchall():
    print(q)
conn.commit()
conn.close()