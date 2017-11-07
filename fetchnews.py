import requests
import pandas as pd
from datetime import datetime
from functools import reduce

def get_sources():
    source_url = 'https://newsapi.org/v1/sources?language=en'
    response = requests.get(source_url).json()
    sources = []
    for source in response['sources']:
        sources.append(source['id'])
    return sources

def get_news(responses):
    sources = get_sources()
    key = "f1ed47573d904a988baf98f093f11086"
    url = 'https://newsapi.org/v1/articles?source={0}&sortBy={1}&apiKey={2}'
    for source in sources:
        try:
            u = url.format(source, 'top',key)
            response = requests.get(u)
            r = response.json()
            for article in r['articles']:
                article['source'] = source
            responses.append(r)
        except:
            u = url.format(source, 'latest', key)
            response = requests.get(u)
            r = response.json()
            for article in r['articles']:
                article['source'] = source
            responses.append(r)

responses = []
get_news(responses)

# Após extração das notícias, coloque em um dataframe
news = pd.DataFrame(reduce(lambda x,y: x+y ,map(lambda r: r['articles'], responses)))
news.to_csv('noticias.csv')