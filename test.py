import datetime
import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

titles = []
url = 'https://www.imdb.com/search/title/?title_type=feature&year=2023-01-01,2023-06-18&start=451&ref_=adv_nxt'
today = datetime.date.today()
tomorrow = datetime.date.today() - datetime.timedelta(days=168)
page = requests.get(url)
soup = BeautifulSoup(page.text,  "html.parser")
movie_box = soup.find_all('div', class_ = 'lister-item mode-advanced')
for box in movie_box:

    if box.find('div', class_ = 'lister-item-content') is not None:
        title = box.find('div > div > p')
        titles.append(title)
    else:
        titles.append('None')

print(titles)