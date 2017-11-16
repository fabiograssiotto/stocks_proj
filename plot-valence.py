import matplotlib.pyplot as plt
import seaborn as sns
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
df = pd.read_sql_query('SELECT publication_date, valence FROM news_table WHERE ticker="{0}"'.format(sys.argv[1]), engine)
#df.set_index('publication_date')
df['publication_date'] = pd.to_datetime(df['publication_date'])
df.sort_values(by='publication_date')

plt.scatter(df['publication_date'].values, df['valence'].values, s =100, c = 'red')
plt.show()
