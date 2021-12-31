import numpy as np
from numpy.lib.function_base import append
import pandas as pd
import itertools

import nltk
# nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.lib.io.file_io import copy

def toLowerAndSplit(tweet):
    tweet = tweet.lower()
    tweet = tweet.split()
    return tweet

def removeNoiseFromTweet(word_list):

    sw = stopwords.words("english")
    twitter_elements = ["rt", "rts", "retweet"]
    i_elements = ["i", "i'm", "im", "iam"] # remove u?

    cleaned_word_list = []
    for element in word_list:
        for word in element:
            #Removes words contained in stopwords
            if word not in sw:
                #Removes words with @ --> remove Tags
                if "@" not in word: 
                    #Removes words containing http --> links
                    if "http" not in word:
                        hasTwitterElement = False
                        hasIElement = False
                        #Removes Twitter exclusive Words (retweet/ rt...) 
                        for tw in twitter_elements:
                            if tw in word:
                                hasTwitterElement = True
                        for ie in i_elements:
                            if ie in word:
                                hasIElement = True
                        if hasTwitterElement == False & hasIElement == False:
                            #Remove special characters from string
                            cleaned_word = ""
                            cleaned_word = "".join(character for character in word if character.isalnum())
                            
                            if cleaned_word != "":
                                if cleaned_word == "":
                                    print("cleaned_word")
                                cleaned_word_list.append(cleaned_word)
    return cleaned_word_list


def makeString(column):
    result = " ".join(column)
    return result

def stemWords(tweet):
    stemmer = PorterStemmer()
    word_stems = []
    for word in tweet:
        word_stems.append(stemmer.stem(word))
    return word_stems


def prepare_model_data(dir):
    df = pd.read_csv(dir)
    
    tweets = pd.DataFrame(df["tweet"].apply(toLowerAndSplit))
    cleaned_words_df = tweets.apply(func=removeNoiseFromTweet, axis=1)
    word_stems = cleaned_words_df.apply(stemWords)
    word_stems_text = word_stems.apply(makeString)

    #split into train and test set
    x_train, x_val, y_train, y_val = train_test_split(word_stems_text, df["class"], 
        test_size=0.2, random_state=10)

    # print(tokenizer.word_counts)

    return x_train, x_val, y_train, y_val   

def prepare_tweet(tweet):
    casted_tweet = toLowerAndSplit(tweet)
    denoised_tweet = removeNoiseFromTweet(casted_tweet)
    stemmed_tweet = stemWords(denoised_tweet)
    stemm_text_tweet = makeString(tweet)
    return stemm_text_tweet
