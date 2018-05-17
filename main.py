#!/usr/bin/env python

import tweepy, sys, os
import matplotlib.pyplot as plt
from nltk.tokenize import TweetTokenizer
from termcolor import colored
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as stopwordsNLTK
import spacy

def removeStopWords(textlist, stopwords):
    for text in textlist:
        for stopword in stopwords:
            if text.lower()==stopword.lower():
                try:
                    textlist.remove(text)
                except:
                    print()

    return textlist

def removeEntities(text, entities):

    for entity in entities:
        print(entity.text)
        text = text.replace(str(entity.text), ' ')
    return text

def removeSingles(textlist):
    for text in textlist:
        if len(text) == 1:
            try:
                textlist.remove(text)
            except:
                print()

    return textlist

def removeURLS(textlist):
    for text in textlist:
        if text[0:4]=='http':
            try:
                textlist.remove(text)
            except:
                print()

    return textlist
def getAdjectivesAndNouns(textlist):
    for text in textlist:

        try:
            type = wn.synsets(text)[0].pos()
            if type =='v' or type=='n':
                continue
            else:
                textlist.remove(text)
        except:
            textlist.remove(text)
    return textlist

def removeSearchTermAndTags(textlist, searchTerm):
    tknizer = TweetTokenizer()
    searchTerm = tknizer.tokenize(searchTerm)
    for text in textlist:
        for term in searchTerm:
            if text.lower()==term.lower():
                try:
                    textlist.remove(text)
                except:
                    print()
    for text in textlist:
        if text[0]=='@':
            try:
                textlist.remove(text)
            except:
                print()
    for text in textlist:
        if text[0]=='#':
            try:
                textlist.remove(text)
            except:
                print()
    return textlist

def percentage(part, whole):
    return 100 * float(part) / float(whole)

intro = '''

___ _ _ _ _ ___ ___ ____ ____    ____ ____ _  _ ___ _ _  _ ____ _  _ ___ ____ _       ____ _  _ ____ _    _   _ ____ _ ____    ___ ____ ____ _
 |  | | | |  |   |  |___ |__/    [__  |___ |\ |  |  | |\/| |___ |\ |  |  |__| |       |__| |\ | |__| |     \_/  [__  | [__      |  |  | |  | |
 |  |_|_| |  |   |  |___ |  \    ___] |___ | \|  |  | |  | |___ | \|  |  |  | |___    |  | | \| |  | |___   |   ___] | ___]     |  |__| |__| |___
'''

developers = '''
  __                                                                _
 /  \ /\   _|_|_  _ .__o  /\  _|_  _    ._ |\ | _ | .__. _|_ o ()  / \ _ _.._ _  _.
| (|//--\|_||_| |(_)|_>o /--\_>| |(_)|_||o | \|(_)|<|(_|_>| || (_X \_/_>(_|| | |(_|
 \__                                     /


'''
print (colored(intro, 'blue'))

print(colored(developers, 'green'))

consumerKey = "UPkTpBcmwlmEbycSAsVpZckDK"
consumerSecret = "9LpMalhBnQrBxyDB1sdXav2HzWW7L4lh2X134KbSrg77ppnmF6"
accessToken = "633164510-zHpOWsTT5fAUNQyjlYvaR3CvvAMBV5LkSTXgJ54l"
accessTokenSecret = "0X8DaYH5lT6avELPUUv9ZGgDAmfbuDB9irtYJJOcFMAzi"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

positivesFile = open('positive-words.txt', 'r')
positiveWords = positivesFile.read().splitlines()

negativesFile = open('negative-words.txt', 'r')
negativeWords = negativesFile.read().splitlines()

stopwordsFiles = open('stopwords.txt', 'r')
stopwords = stopwordsFiles.read().splitlines()


spacyParser = spacy.load('en')
tweetTokenizer = TweetTokenizer()

searchTerm = input("Enter keyword/hashtag to search about: ")
noOfSearchTerms = int(input("Enter how many tweets to analyze: "))

veryPositive =0
positive = 0
negative = 0
veryNegative=0
neutral = 0
polarity = 0



tweets = tweepy.Cursor(api.search, q=searchTerm, count=100,
                           lang="en",
                           since="2017-04-03").items(noOfSearchTerms)
for tweet in tweets:

    print('-------------------------------------------')

    print(tweet.text)
    tweetPolarity =0
    entities = list(spacyParser(tweet.text).ents)
    # print(entities)
    tweetWords = removeEntities(tweet.text, entities)
    # print(tweetWords)
    tweetWords = tweetTokenizer.tokenize(tweetWords)
    # print(tweetWords)
    tweetWords = removeStopWords(tweetWords, stopwords)
    # print(tweetWords)

    tweetWords = removeStopWords(tweetWords, stopwordsNLTK.words('english'))
    # print(tweetWords)

    tweetWords = removeSearchTermAndTags(tweetWords, searchTerm)
    # print(tweetWords)
    tweetWords = removeURLS(tweetWords)
    # print(tweetWords)
    tweetWords = removeSingles(tweetWords)
    # print(tweetWords)
    tweetWords = getAdjectivesAndNouns(tweetWords)
    print(tweetWords)
    print('-------------------------------------------')

    for tweetWord in tweetWords:

        for positiveWord in positiveWords:
            if tweetWord==positiveWord:
                tweetPolarity += 1

        for negativeWord in negativeWords:
            if tweetWord == negativeWord:
                tweetPolarity -= 1

    if tweetPolarity > 1:
        veryPositive+=1
    elif tweetPolarity == 1:
        positive+=1
    elif tweetPolarity == 0:
        neutral +=1
    elif tweetPolarity == -1:
        negative += 1
    elif tweetPolarity < -1:
        veryNegative +=1


positive = percentage(positive, noOfSearchTerms)
negative = percentage(negative, noOfSearchTerms)
neutral = percentage(neutral, noOfSearchTerms)

veryPositive = percentage(veryPositive, noOfSearchTerms)
veryNegative = percentage(veryNegative, noOfSearchTerms)


positive = format(positive, '.2f')
neutral = format(neutral, '.2f')
negative = format(negative, '.2f')
veryNegative = format(veryNegative, '.2f')
veryPositive = format(veryPositive, '.2f')

print("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " Tweets.")

labels = ['Very Positive [' + str(veryPositive) + '%]','Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]', 'Very Negative [' + str(veryNegative) + '%]',]
sizes = [veryPositive, positive, neutral, negative, veryNegative]
colors = ['yellowgreen', 'gold', 'red', 'orange', 'blue']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " Tweets.")
plt.axis('equal')
plt.tight_layout()
plt.show()
