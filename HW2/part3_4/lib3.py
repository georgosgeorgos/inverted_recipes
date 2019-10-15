import numpy as np
import re
import time
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from unidecode import unidecode


def processTitle(title):

    if type(title) != str:
        title = str(title)

    new = title.lower()
    new = unidecode(new)
    new = re.sub("bbc food - recipes -", "", new)
    wordList = re.sub("[^\w-]", " ", new).split()
    wordList = [i.strip() for i in wordList]

    return wordList


def stopWords(text):

    for word in text:  # iterate over word_list
        if word in stopwords.words("english") or word in stopwords.words("italian"):

            text.remove(word)  # remove word from filtered_word_list if it is a stopword
    return text


def wordTokenizerPunctuation(text):
    """
    this version conserve original punctuation
    """
    filteredText = text[:]  # make a copy of the word_list
    filteredText = filteredText.lower()
    wordList = re.sub("', '|\[|\]|'", " ", filteredText).split()

    return wordList


def wordTokenizer(text):

    # print(type(text))
    if type(text) != str:
        text = str(text)
    # print(type(text))

    text = text.lower()
    wordList = re.sub("[^\w-]", " ", text).split()
    wordList = [i.strip() for i in wordList]

    return wordList


def wordTokenizerImproved(text):

    # print(type(text))
    if type(text) != str:
        text = str(text)
    # print(type(text))

    text = text.lower()
    text = unidecode(text)
    wordList = re.sub("[^\w-]", " ", text).split()
    wordList = [i.strip() for i in wordList]

    return wordList


def stemmerPorter(text):

    stemmer = PorterStemmer()

    stemmed = [stemmer.stem(word) for word in text]

    return stemmed


def stemmerLancaster(text):

    stemmer = LancasterStemmer()

    stemmed = [stemmer.stem(word) for word in text]

    return stemmed


def Lemmatize(text):

    wordnet_lemmatizer = WordNetLemmatizer()

    lemm = [wordnet_lemmatizer.lemmatize(word, pos="v") for word in text]

    return lemm


def preprocess(text):

    filteredText = text[:]
    filteredText = wordTokenizerImproved(filteredText)
    filteredText = stopWords(filteredText)
    filteredText = Lemmatize(filteredText)  # the order is important!!!
    filteredText = stemmerLancaster(filteredText)
    # filteredText = stopWords(filteredText)

    return filteredText


def preprocessTitle(text):

    filteredText = text[:]
    filteredText = processTitle(filteredText)
    filteredText = stopWords(filteredText)
    filteredText = Lemmatize(filteredText)
    filteredText = stemmerLancaster(filteredText)
    # filteredText = stopWords(filteredText)

    return filteredText
