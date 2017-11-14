# Script para executar classificação das manchetes relacionadas a ações.
import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
from pandas import DataFrame


def create_label(row):
    if (row['PosScore']-row['NegScore']) == 0:
        return 'Neutral'
    elif (row['PosScore']-row['NegScore']) > 0:
        return 'Positive'
    else:
        return 'Negative'

# Leitura do sentiwordnet 3.0 em um dataframe e manipulação dos dados.
# Após a manipulação ficamos com as colunas na tabela: Pos Neg Word
df = pd.read_csv('SentiWordNet_3.0.0_20130122.txt', comment = '#', sep='\t')
df.drop(df.columns[[0, 1, 5]], axis=1, inplace=True)
df.drop(df.tail(1).index,inplace=True)

# Processamento do wordnet para obter um label único para cada palavra...
df['label'] = df.apply (lambda row: create_label (row),axis=1)

# Test Data
engine = create_engine('sqlite:///news.db')
table_name = 'news_table'
test_df = pd.read_sql_table(table_name, engine)


vectorizer = CountVectorizer()

train_data = df['SynsetTerms']
train_labels = df['label']
test_data = test_df['title']
test_data = test_data.loc[0:9]
train_vectors = vectorizer.fit_transform(train_data.values.astype('U'))
test_vectors = vectorizer.transform(test_data.values.astype('U'))

# Classificação
classifier = svm.SVC(kernel='linear')
classifier.fit(train_vectors, train_labels)
prediction = classifier.predict(test_vectors)
