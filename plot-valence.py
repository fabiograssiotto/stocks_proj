import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import sys

def get_graph_data(ticker):
    df = pd.read_sql_query('SELECT publication_date, valence, title FROM news_table WHERE ticker="{0}"'.format(ticker), engine)
    df['publication_date'] = pd.to_datetime(df['publication_date'])
    df['date_num'] = df.publication_date.values.astype('datetime64[s]').astype('int')
    df.sort_values(by='publication_date')

    # Remove dados esparsos antes de 2016.
    df = df[(df['publication_date'].dt.year > 2016)]
    # Agrega valências por dia
    return df.groupby([pd.Grouper(freq='D',key='publication_date')]).mean()

engine = create_engine('sqlite:///news.db')

fig = plt.figure()
fig.suptitle('Valências de notícias de ações', fontsize=16)

ticker_lst = ['AAPL', 'CSCO', 'FB', 'GOOGL', 'IBM', 'INTC', 'MSFT', 'ORCL', 'SAP', 'TSM']
subplot_num = 1
for ticker in ticker_lst:
    a = get_graph_data(ticker)
    ax = fig.add_subplot(2, 5, subplot_num)
    ax = sns.regplot(x='date_num', y='valence', data=a, order=1)
    ax.set_title("Valência das noticías para {0}".format(ticker))
    ax.set_xlabel('Data')
    ax.set_ylabel('Valência')
    subplot_num = subplot_num + 1

plt.show()