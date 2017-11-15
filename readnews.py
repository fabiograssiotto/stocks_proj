# -*- coding: utf-8 -*-
# 
# 

import csv
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import NaiveBayesClassifier
from nltk.stem import RSLPStemmer
from nltk.corpus import wordnet as wordnet
from nltk.corpus import sentiwordnet as swn
import nltk
import matplotlib.pyplot as pyplot
import numpy as np
import datetime
import time
import os.path
import pandas as pd


def wordnet_pos_code(tag):
    '''Translation from nltk tags to Wordnet code'''
    if tag.startswith('NN'):
        return wordnet.NOUN
    elif tag.startswith('VB'):
        return wordnet.VERB
    elif tag.startswith('JJ'):
        return wordnet.ADJ
    elif tag.startswith('RB'):
        return wordnet.ADV
    else:
        return ''

def pos_tag(sentence):
    '''POS tagging of a sentence.'''
    tagged_words = []
    tokens = nltk.word_tokenize(sentence)
    tag_tuples = nltk.pos_tag(tokens)
    for (string, tag) in tag_tuples:
        token = {'word':string, 'pos':tag}            
        tagged_words.append(token)    
    return tagged_words

def word_sense_cdf(word, context, wn_pos):
    '''Word sense disambiguation in terms of matching words frequency 
    between the context each sense's definition. Adapted from
    www.slideshare.net/faigg/tutotial-of-sentiment-analysis'''
    senses = wordnet.synsets(word, wn_pos)
    if len(senses) > 0:
        cfd = nltk.ConditionalFreqDist((sense, def_word)
                       for sense in senses
                       for def_word in sense.definition().split()
                       if def_word in context)
        best_sense = senses[0]
        for sense in senses:
            try:
                if cfd[sense].max() > cfd[best_sense].max():
                    best_sense = sense
            except: 
                pass                
        return best_sense
    else:
        return None

def word_sense_similarity(word, context, dummy = None):
    '''Another word sense disambiguation technique. It's VERY SLOW.
    Adapted from: pythonhosted.org/sentiment_classifier'''
    wordsynsets = wordnet.synsets(word)
    bestScore = 0.0
    result = None
    for synset in wordsynsets:
        for w in nltk.word_tokenize(context):
            score = 0.0
            for wsynset in wordnet.synsets(w):
                sim = wordnet.path_similarity(wsynset, synset)
                if(sim == None):
                    continue
                else:
                    score += sim
            if (score > bestScore):
                bestScore = score
                result = synset
    return result

def sentiwordnet_classify(text):
    '''Breaks a multi sentence text to separate sentences.
    This improves context for the word sense disambiguation.
    Returns a class'''
    score_tot = 0
    score_tot_thr = 0
    class_tot = 0
    class_tot_thr = 0
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        (score, score_thr) = sentence_score(sentence)
        score_tot += score
        score_tot_thr += score_thr

    #Trust the thresholded value more when classifying
    if score_tot_thr != 0:
        clss = 'pos' if score_tot_thr > 0 else 'neg'
    elif score_tot != 0:
        clss = 'pos' if score_tot > 0 else 'neg'
    else:
        clss = None
    return clss

def sentence_score(text, threshold = 0.75, wsd = word_sense_cdf):
    '''Classifies a phrase according to sentiment analysis based
    on WordNet and SentiWordNet. It also computes a thresholded 
    score by ignoring strongly objective words.'''
    tagged_words = pos_tag(text)

    obj_score = 0 # object score 
    pos_score=0 # positive score
    neg_score=0 #negative score
    pos_score_thr=0
    neg_score_thr=0

    for word in tagged_words:
    #     print word
        if 'punct' not in word :
            sense = wsd(word['word'], text, wordnet_pos_code(word['pos']))
            if sense is not None:
                sent = swn.senti_synset(sense.name())
                if sent is not None and sent.obj_score() != 1:
                    obj_score = obj_score + float(sent.obj_score())
                    pos_score = pos_score + float(sent.pos_score())
                    neg_score = neg_score + float(sent.neg_score())
                    if sent.obj_score() < threshold:
                        pos_score_thr = pos_score_thr + float(sent.pos_score())
                        neg_score_thr = neg_score_thr + float(sent.neg_score())

    return (pos_score - neg_score, pos_score_thr - neg_score_thr)



# Leitura do arquivo Apple.csv.
#
# ,figi,figi_ticker,publication_date,summary,ticker,title,url
# row[0] indice
# row[1] figi
# row[2] figi_ticker
# row[3] publication_date
# row[4] summary
# row[5] ticker
# row[6] title
# row[7] url
with open('news/GOOGL.csv', encoding='utf8') as csvFile:
    readCsv = csv.reader(csvFile, delimiter=',',  quotechar="\"")
    next(readCsv, None)
    figi_ticker = []
    dates = []
    ticker = []
    title = []
    score = []
    score_thr = []
    count = 0
    for row in readCsv:
#        printProgressBar(count, 499, prefix = 'Lendo Manchetes: ', suffix = 'OK', length = 50)
        #a_date = row[3]
        dates.append(row[3][0:10])
        ticker.append(row[5])
        aux = row[6].lower()
        # Remover nesta etapa de pre-processamento as 'stopwords' para restringir a análise, e fazer todas as palavras minúsculas.
        stop_words = stopwords.words('english')
        tokenizer = RegexpTokenizer(r'\w+')
        # Considere apenas os stems das palavras para melhorar o score de valência.
        st = RSLPStemmer()
        #content = [word.lower() for word in tokenizer.tokenize(aux) if word.lower() not in stop_words]
        #content = [st.stem(word.lower()) for word in aux if word.lower() not in stop_words]
        #title.append(content)
        title.append(row[6])
        (aux2, aux3) = sentence_score(aux)
        score.append(aux2)
        score_thr.append(aux3)
        #print (dates[count], "\n")
        #print (ticker[count], "\n")
        #print (title[count], "\n")
        #print (sentence_score(aux))
        #print (score[count], "\n")
        #print (score_thr[count], "\n")
    
        count = count + 1
        time.sleep(0.001)
csvFile.close()
data = [dates,ticker,title,score,score_thr]
df = pd.DataFrame(data,columns=['Date','Stock','Title','Score','Score_Thr'])
print (df)

#for i in range(0, 20):
#    print (dates[i], " ", ticker[i], " ", title[i])

    
