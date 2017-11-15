# Script para criar um banco de dados sql-lite com as notícias relativas
# às ações de tecnologia.

import glob
import pandas as pd
from sqlalchemy import create_engine

news_files = glob.glob('news/*.csv')

# Conexão com db
disk_engine = create_engine('sqlite:///news.db')

for file in news_files:
    df = pd.read_csv(file)
    df = df[['ticker', 'publication_date', 'title']]
    df.to_sql('news_table', disk_engine, if_exists='append')
    