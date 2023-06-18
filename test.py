import datetime
import numpy as np
pages = np.arange(1, 9, 50)
today = datetime.date.today()
tomorrow = datetime.date.today() - datetime.timedelta(days=168)
url = [f'https://www.imdb.com/search/title/?title_type=feature&year=2023-01-01,{today}&start={i:d}&ref_=adv_nxt'  for i in (range(1,500, 50))]

print(url)