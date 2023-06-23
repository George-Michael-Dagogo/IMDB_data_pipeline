import datetime
import numpy as np
from bs4 import BeautifulSoup

from prefect import Flow,task
import datetime
from prefect.schedules import IntervalSchedule

#incase if your fucntion has a slight 
@task(max_retries=3, retry_delay=datetime.timedelta(seconds=5))
def lets_goo():
    x = str(input('what is your name:'))
    y = str(input('what is your gender choose male or female ')).lower()
    if y == 'male':
        print('Welcome Mr', x)
    elif y == 'female':
        print('Welcome Mrs/Miss',x)
    elif y == 'they/them':
        print('This program cannot handle the complexities of that spectrum')
   


def flow_caso(schedule=None):
    with Flow("wellllll",schedule=schedule) as flow:
        lets_go = lets_goo()
    return flow


schedule = IntervalSchedule(
    start_date = datetime.datetime.now() + datetime.timedelta(seconds = 2),
    interval = datetime.timedelta(hours=3)
)
flow=flow_caso(schedule)

flow.run()