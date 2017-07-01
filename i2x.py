
# coding: utf-8

# In[15]:

# Copyright 2017-2017 by Fabricio Amaral. All Rights Reserved.

import nltk
from nltk.corpus import stopwords
from collections import defaultdict, Counter
import operator
import math

# importing a text pair
def import_script_transcript(s = 'path_to_script', t = 'path_to_transcript'):
    global script 
    script = []
    with open(s) as s:
         script = s.readlines()

    global transcript 
    transcript = []  
    with open(t) as t:
         transcript = t.readlines()   

def get_corpus_script():
    # remove common words and tokenize
    stoplist = stopwords.words('english') + ['many', 'may', 'also', 'used', 'foods', '–']
    # corpus_script pre processing
    corpus_script = [[word for word in document.lower().split() if word not in stoplist]
                      for document in script]
    
    return corpus_script

# getting the transciption corpus
def get_transciption_corpus():
    # remove common words and tokenize
    stoplist = stopwords.words('english') + ['many', 'may', 'also', 'used', 'foods', '–']
    # corpus_script pre processing
    corpus = [[word for word in document.lower().split() if word not in stoplist]
               for document in transcript]

    return sum(corpus, [])    
        
# selection the keywords
def get_keywords(n):
    corpus_script = get_corpus_script()
    # remove words that appear only once
    frequency = defaultdict(int)
    for text in corpus_script:
        for token in text:
            frequency[token] += 1
    # frequency control  
    corpus_script = [[token for token in text if frequency[token] > 1]
                      for text in corpus_script]

    # list of tuples sorted by the second element 'itemgetter(1)' in each tuple.
    frequency_list = sorted(frequency.items(), key = operator.itemgetter(1))
    frequency_list.reverse()
    # getting the first element in a list of tuples
    frequency_list = [str(i[0]) for i in frequency_list]
    keywords = frequency_list[0:n]
    
    return keywords

# comparison method: cossine similarity
def cosdis(v1, v2):
    common = v1[1].intersection(v2[1])
    
    return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]

def word2vec(word):
    cw = Counter(word)
    sw = set(cw)
    lw = math.sqrt(sum(c * c for c in cw.values()))
    if lw == 0:
        lw = lw + 0.0001
        
    return cw, sw, lw

def removePunctuations(str_input):
    ret = []
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for char in str_input:
        if char not in punctuations:
            ret.append(char)
            
    return "".join(ret)

def main(keywords_number):
    corpus = get_transciption_corpus()   
    keywords = get_keywords(keywords_number)
    for i in keywords:
        for j in corpus:
            print('(%s , %s) = %.2f' % (i, j, cosdis(word2vec(removePunctuations(i)), word2vec(removePunctuations(j)))))
            

