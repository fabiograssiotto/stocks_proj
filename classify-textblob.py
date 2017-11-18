# Script para executar classificação das manchetes relacionadas a ações.
import pandas as pd
from sqlalchemy import create_engine
from textblob import TextBlob

# Test Data
engine = create_engine('sqlite:///news.db')
table_name = 'news_table'
test_df = pd.read_sql_table('news_table', engine)

test_df['valence'] = test_df.apply(lambda x: TextBlob(x['title']).sentiment.polarity, axis=1)
# Escreve a classificação no banco de dados.
test_df = test_df.drop('index', axis = 1)
test_df.to_sql('news_table', engine, if_exists='replace')