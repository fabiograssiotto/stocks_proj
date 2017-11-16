import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import sys

if len(sys.argv) != 2 :
    print ("Usage: plot-valence.py TICKER")
    sys.exit()
else:
    print ("Valence plot for {0}".format(sys.argv[1]))

engine = create_engine('sqlite:///news.db')
table_name = 'news_table'
df = pd.read_sql_query('SELECT publication_date, valence, title FROM news_table WHERE ticker="{0}"'.format(sys.argv[1]), engine)
df['publication_date'] = pd.to_datetime(df['publication_date'])
df['date_num'] = df.publication_date.values.astype('datetime64[s]').astype('int')

df.sort_values(by='publication_date')

# Remove duplicados e agrega valências em dias.
df = df.drop_duplicates(subset='title', keep="last")
a = df.groupby([pd.Grouper(freq='D',key='publication_date')]).mean()
plt.plot(a['valence'], c = 'red')
plt.show()
