import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def get_classifier():
    df = pd.read_sql_query('SELECT classifier FROM classifier_table', engine)
    return df.iloc[0]['classifier']

def get_valence_data(ticker):
    df = pd.read_sql_query('SELECT publication_date, valence, title FROM news_table WHERE ticker="{0}"'.format(ticker), engine)
    df['publication_date'] = pd.to_datetime(df['publication_date'])
    df['date_num'] = df.publication_date.values.astype('datetime64[s]').astype('int')
    df.sort_values(by='publication_date')

    df.query("publication_date >= '{0}' and publication_date <= '{1}'".format(date_from, date_to), inplace=True)
    # Agrega valências por dia
    return df.groupby([pd.Grouper(freq='D',key='publication_date')]).mean()

date_from = "19700101"
date_to = "20171231"

engine = create_engine('sqlite:///news.db')

sns.set_style("white")
fig, ax1 = plt.subplots(figsize=(15,10))

fig.suptitle('Valências de Notícias, Classificador {0}'.format(get_classifier()), fontsize=20)

ticker_lst = ['AAPL', 'CSCO', 'FB', 'GOOGL', 'IBM', 'INTC', 'MSFT', 'ORCL', 'SAP', 'TSM']

for ticker in ticker_lst:
    plot_df = get_valence_data(ticker)
    plot_df.dropna()
    
    ax1.set_ylabel('Valência')
    ax1.set_xlabel('Data')

    g = sns.stripplot(x=plot_df.index, y=plot_df.valence, data=plot_df, size=10, ax = ax1, color=sns.color_palette("deep")[np.random.randint(6)])
    g.set(xticklabels=[])

plt.show()
