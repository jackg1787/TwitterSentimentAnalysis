import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
#import csv

class TwitterClient(object):
    
    # define the init- this runs whenever the twitter client class is called (initialise the class)
    def __init__(self):
        
        #Keys used to connect to twitter api
        consumer_key = 'XhsHQATnYEbbqWB1hUz12WkHO'
        consumer_secret = '8aulITTTl7uIxxp7zha2XoFbqSNhNkECSunhtTvHK1keai8Ba0'
        access_token = '913672504224419840-F7hlmKusX0xoZ3kxR6AfADZrIeoXjod'
        access_token_secret = 'kcr8ec1RdPLhTTqSEI0NV7kGlXpqkT0gLLDIOplTWk3sT'
        
        # try to connect
        try:
            # pass in keys and token, then use tweepy package to connect
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Something went wrong with authentication step")
    
    # define all the functions to be used in the main():
    
    #defime function to  get the tweets
    def GetTweets(self, query, count = 10):
        # set up some arrays for the data
        tweets = []
        tweetdictionary = []
        tweetsentiment = []
        # actually call the api for the tweets
        rawtweets = self.api.search(q = query, count = count)
        for tweet in rawtweets:
            if tweet not in tweets:
                # make multidimentional array of who tweeted what
                screenname = "("+ tweet.user.screen_name+ ")"
                #get sentiment of tweets using function below
                sentiment = self.get_tweet_sentiment(tweet.text)
                # put all info in one dictionary if further analysis is needed
                cleanedtweet = self.clean_tweet(tweet.text)
                tweetdictionary.append([tweet.user.name,screenname,cleanedtweet, sentiment])
                #raw list of tweets
                tweets.append(tweet.text)
                # raw list of sentiments
                tweetsentiment.append(sentiment)
        # setting up an object to hold each of the different objects        
        dictionary = {"tweets":tweets , "tweetdictionary":tweetdictionary, "tweetsentiment":tweetsentiment}
        
        return(dictionary)
        
    # defime function to clean the tweets of all bullshit stuff  
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    # work out the sentiment of the tweets using text blob package
    def get_tweet_sentiment(self, tweet):
        tweetpolarity = TextBlob(self.clean_tweet(tweet))
        return tweetpolarity.sentiment.polarity
    
    #add a function to see hwere people are tweeting from using the lang setting.

        
    
    
    
    
    
    
#main - actually run the program, call the functions above etc
def main(): 
    # call the connect to wtitter function
    api = TwitterClient()
    # get the tweets using the get tweets function
    tweets = api.GetTweets(query ='liverpool man city', count = 100)
    #print(tweets["tweetsentiment"])
    # work out average sentiment
    averageSentiment = sum(tweets["tweetsentiment"])/len(tweets["tweetsentiment"])
    
    not0 = []
    neutral = 0
    positive = 0
    negative = 0
    
    #count neutral, positive, negative tweets
    for i in range(len(tweets["tweetsentiment"])):
        if str(tweets["tweetsentiment"][i]) != '0.0':
            not0.append(tweets["tweetsentiment"][i])

    for i in range(len(tweets["tweetsentiment"])):
        if tweets["tweetsentiment"][i] >0.0:
            positive = positive +1

    for i in range(len(tweets["tweetsentiment"])):
        if tweets["tweetsentiment"][i] <0.0:
            negative = negative + 1
            
    for i in range(len(tweets["tweetsentiment"])):
        if tweets["tweetsentiment"][i] == 0.0:
            neutral = neutral + 1
                   
    # average sentiment for non neutral tweets    
    averageSentimentNoNeutral = sum(not0)/len(not0)
    # percent of tweets tat are negative, neutral, positive
    neutralPercent = 100*neutral/len(tweets["tweetsentiment"])
    positivePercent= 100*positive/len(tweets["tweetsentiment"])
    negativePercent= 100*negative/len(tweets["tweetsentiment"])
    
    print("Average Sentiment Including neutral tweets: ", averageSentiment)
    print("Average Sentiment NOT including neutral tweets: ",averageSentimentNoNeutral)
    print("Percent of tweets that are positive: ", positivePercent)
    print("Percent of tweets that are negative: ", negativePercent)
    print("Percent of tweets that are neutral: ", neutralPercent)
    print(tweets["tweetdictionary"])
    
    #for tweet in tweets:
     #   print(tweets["tweetdictionary"])
    
    
    
    # write results to file to check
    #myFile = open('example2.csv', 'w', encoding = 'utf-8')
    #with myFile:
    #    writer = csv.writer(myFile)
    #    writer.writerows(tweets["tweetdictionary"])
     
   # print("Writing complete")
    
    
if __name__ == "__main__":
    # calling main function
    main()              