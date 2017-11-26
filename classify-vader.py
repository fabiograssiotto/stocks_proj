# Script para executar classificação das manchetes relacionadas a ações.
import pandas as pd
from sqlalchemy import create_engine
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Test Data
engine = create_engine('sqlite:///news.db')
table_name = 'news_table'
test_df = pd.read_sql_table('news_table', engine)

vader = SentimentIntensityAnalyzer()

test_df['valence'] = test_df.apply(lambda x: vader.polarity_scores(x['title'])['compound'], axis=1)

# Output
print(test_df['valence'].value_counts())

# Escreve a classificação no banco de dados.
test_df = test_df.drop('index', axis = 1)
test_df.to_sql('news_table', engine, if_exists='replace')

# Cria tabela para identificar o classificador empregado.
class_df = pd.DataFrame(['VADER'], columns=['classifier'])
class_df.to_sql('classifier_table', engine, if_exists='replace')