import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
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

# Verifica argumentos de chamada
num_params = len(sys.argv)
if num_params == 1:
    # desde o inicio dos tempos :)
    date_from = "19700101"
    date_to = "20171231"
elif num_params == 2 and sys.argv[1] == '-h':
    print("Uso: plot-graphs.py YYYY-MM-DD plota desde a data")
    print("     plot-graphs.py YYYY-MM-DD YYYY2-MM2-DD2 entre datas")
    print("     plot-graphs.py Sem argumentos, plota a base toda.")
    sys.exit()
elif (num_params == 2):
    date_from = sys.argv[1]
    date_to = "20171231"
else:
    date_from = sys.argv[1]
    date_to = sys.argv[2]

engine = create_engine('sqlite:///news.db')

sns.set_style("white")
fig, axs = plt.subplots(2,5, figsize=(15,10))

if len(sys.argv) == 1:
    fig.suptitle('Valências de Notícias e Valores de Ações, Classificador {0}'.format(get_classifier()), fontsize=20)
else:
    fig.suptitle('Valências de Notícias e Valores de Ações desde {0}, Classificador {1}'.format(date_from, get_classifier()), fontsize=20)

ticker_lst = ['AAPL', 'CSCO', 'FB', 'GOOGL', 'IBM', 'INTC', 'MSFT', 'ORCL', 'SAP', 'TSM']

subplot_line = 0
subplot_col = 0

for ticker in ticker_lst:
    valence_data = get_valence_data(ticker)
    ticker_data = pd.read_csv("nasdaqHistorical/{0}_Historical.csv".format(ticker))
    ticker_data.date = pd.to_datetime(ticker_data.date)
    ticker_data.sort_values(by='date')
    ticker_data = ticker_data.set_index(ticker_data.date)

    # Concatena dados e remove linhas sem informação
    plot_df = pd.concat([valence_data, ticker_data], axis=1)
    plot_df = plot_df.dropna()
    plot_df = plot_df[['close', 'valence']]

    # Para contornar erros de tipo na planilha de valor das ações.
    plot_df['close'] = plot_df['close'].astype(str).astype(float)
    plot_df['date'] = plot_df.index
    plot_df['date_f'] = pd.factorize(plot_df['date'])[0] + 1
    mapping = dict(zip(plot_df['date_f'], plot_df['date'].dt.date))
    
    ax1 = axs[subplot_line][subplot_col]
    ax2 = ax1.twinx()
    ax1.set_title(ticker)
    ax1.set_ylabel('Valência')
    ax1.set_xlabel('Data')
    ax2.set_ylabel('Preço Ação')


    sns.regplot(x=plot_df.date_f, y=plot_df.valence, data=plot_df, ax = ax1, color="b", order=1)
    sns.tsplot(data=plot_df.close, time=plot_df.date_f, ax = ax2, color="r")
    subplot_col = subplot_col + 1;
    if (subplot_col > 4):
        subplot_col = 0
        subplot_line = 1

plt.show()
