from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt


def percentage(part, whole):
    return 100 * float(part) / float(whole)


consumerKey = "UPkTpBcmwlmEbycSAsVpZckDK"
consumerSecret = "9LpMalhBnQrBxyDB1sdXav2HzWW7L4lh2X134KbSrg77ppnmF6"
accessToken = "633164510-zHpOWsTT5fAUNQyjlYvaR3CvvAMBV5LkSTXgJ54l"
accessTokenSecret = "0X8DaYH5lT6avELPUUv9ZGgDAmfbuDB9irtYJJOcFMAzi"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

searchTerm = input("Enter keyword/hashtag to search about: ")
noOfSearchTerms = int(input("Enter how many tweets to analyze: "))
i = 1
positive = 0
negative = 0
neutral = 0
polarity = 0
for tweet in tweepy.Cursor(api.search, q=searchTerm, count=100,
                           lang="en",
                           since="2017-04-03").items(noOfSearchTerms):
    print(tweet.created_at, tweet.text)
    print(i)
    i += 1
    analysis = TextBlob(tweet.text)

    polarity += analysis.sentiment.polarity

    if analysis.sentiment.polarity == 0:
        neutral += 1
    elif analysis.sentiment.polarity < 0:
        negative += 1
    elif analysis.sentiment.polarity > 0:
        positive += 1

positive = percentage(positive, noOfSearchTerms)
negative = percentage(negative, noOfSearchTerms)
neutral = percentage(neutral, noOfSearchTerms)
polarity = percentage(polarity, noOfSearchTerms)

positive = format(positive, '.2f')
neutral = format(neutral, '.2f')
negative = format(negative, '.2f')

print("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " Tweets.")

if polarity == 0.00:
    print("Neutral")
elif polarity < 0.00:
    print("Negative")
elif polarity > 0.00:
    print("Positive")

labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'gold', 'red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " Tweets.")
plt.axis('equal')
plt.tight_layout()
plt.show()
