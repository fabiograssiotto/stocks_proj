# Script para criar um banco de dados sql-lite com as notícias relativas
# às ações de tecnologia.

import glob
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import MetaData

if os.path.exists('news.db'):
    os.remove('news.db')

news_files = glob.glob('news/*.csv')

# Conexão com db
disk_engine = create_engine('sqlite:///news.db')

for file in news_files:
    df = pd.read_csv(file)
    df = df[['ticker', 'publication_date', 'title']]
    # Remove entradas duplicadas
    df = df.drop_duplicates(subset='title', keep="last")
    df.to_sql('news_table', disk_engine, if_exists='append')

m = MetaData()
m.reflect(disk_engine)
print('News Database:')
for table in m.tables.values():
    print("Tabela: {0}".format(table.name))
    print("Colunas:")
    for column in table.c:
        print(column.name)
    