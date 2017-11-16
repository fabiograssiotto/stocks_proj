# Script para executar classificação das manchetes relacionadas a ações.
import pandas as pd
import nltk
import re
from pandas import DataFrame
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
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

# Leitura do sentiwordnet 3.0 em um dataframe e manipulação dos dados.
# Após a manipulação ficamos com as colunas na tabela: Pos Neg Word
df = pd.read_csv('SentiWordNet_3.0.0_20130122.txt', comment = '#', sep='\t')
df.drop(df.columns[[0, 1, 5]], axis=1, inplace=True)
df.drop(df.tail(1).index,inplace=True)

# Processamento do wordnet para obter um label único para cada palavra...
df['label'] = df.apply (lambda row: create_label (row),axis=1)

# Remover os neutros
df = df[df.label != 'Neutral']

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

train_data = df['SynsetTerms']
train_labels = df['label']
test_data = test_df['title']

train_vectors = vectorizer.fit_transform(train_data.values.astype('U'))
test_vectors = vectorizer.transform(test_data.values.astype('U'))

# Classificação
classifier = BernoulliNB()
classifier.fit(train_vectors, train_labels)
prediction = classifier.predict(test_vectors)
probabilities = classifier.predict_proba(test_vectors)

# Transformação de probabilidades do classificador em scores
scores = []
for prob in probabilities:
    if prob[0] >= prob[1]:
        score = (100*(-prob[0]+1)/2)
    else:
        score = (100*(prob[1]+1)/2)
    scores.append(score)


test_df['label'] = prediction  
test_df['valence'] = scores

# Escreve a classificação no banco de dados.
test_df = test_df.drop('index', axis = 1)
test_df.to_sql('news_table', engine, if_exists='replace')