# Script para executar classificação das manchetes relacionadas a ações.
import pandas as pd
import nltk
import re
from pandas import DataFrame
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sqlalchemy import create_engine

# Transforma scores positivos/negativos em label.
def create_label(row):
    if (row['PosScore']-row['NegScore']) == 0:
        return 'Neutral'
    elif (row['PosScore']-row['NegScore']) > 0:
        return 'Positive'
    else:
        return 'Negative'

# Stemming
def stem_tokens(tokens, stemmer):
    stemmed = [stemmer.stem(item) for item in tokens]
    return(stemmed)

# Tokenização
def tokenize(text):
    text = re.sub("[^a-zA-Z]", " ", text)
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return(stems)

# Leitura do AFINN em um dataframe e manipulação dos dados.
# Após a manipulação ficamos com as colunas na tabela: Word Valence
df = pd.read_csv('AFINN-en-165.txt', header=None, sep='\t')

# Test Data
engine = create_engine('sqlite:///news.db')
table_name = 'news_table'
test_df = pd.read_sql_table(table_name, engine)

stemmer = PorterStemmer()

vectorizer = CountVectorizer(
    analyzer = 'word',
    tokenizer = tokenize,
    lowercase = True,
    stop_words = 'english'
)

train_data = df[0]
train_labels = df[1]
test_data = test_df['title']

train_vectors = vectorizer.fit_transform(train_data.values.astype('U'))
test_vectors = vectorizer.transform(test_data.values.astype('U'))

# Classificação
classifier = MultinomialNB()
classifier.fit(train_vectors, train_labels)
prediction = classifier.predict(test_vectors)

# Output
s = pd.Series(prediction)
print(s.value_counts())

test_df['valence'] = prediction  

# Escreve a classificação no banco de dados.
test_df = test_df.drop('index', axis = 1)
test_df.to_sql('news_table', engine, if_exists='replace')

# Cria tabela para identificar o classificador empregado.
class_df = pd.DataFrame(['AFINN'], columns=['classifier'])
class_df.to_sql('classifier_table', engine, if_exists='replace')