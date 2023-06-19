import datetime
import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
pages = np.arange(1, 9, 50)
today = datetime.date.today()
tomorrow = datetime.date.today() - datetime.timedelta(days=168)
#url = [f'https://www.imdb.com/search/title/?title_type=feature&year=2023-01-01,{today}&start={i:d}&ref_=adv_nxt'  for i in (range(1,500, 50))]
url = "https://www.imdb.com/search/title/?title_type=feature&year=2023-01-01,2023-06-18&start=101&ref_=adv_nxt"
votes = []

page = requests.get(url)
soup = BeautifulSoup(page.text,  "html.parser")
movie_box = soup.find_all('div', class_ = 'lister-item mode-advanced')
for box in movie_box:
    if box.find('p', class_ = 'sort-num_votes-visible') is not None:
                #Number of votes
            vote = int(box.find('p', class_ = 'sort-num_votes-visible').text.replace('\n','').replace('Votes:','').replace(',',''))
            votes.append(vote)
    else:
            votes.append(None)
print(votes)