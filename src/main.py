import tweepy
import pandas as pd
import time

# global authentication parameters
consumer_key = "2HqMH7JkCUEeGrMUAgOnvrQVv"
consumer_secret = "DOhOmTDq2IGMPUIKIWGlBX0i03RvA2TuAZ3kCJ9YAbGj4nJL4N"
access_token = "1465920477000605698-WdhsQqcmVv5Qv4mw1LKXPiQMGN9xwd"
access_token_secret = "zhqZfCtzTunJiztXpC3T2nj2XMD9TjdAOyQdsBMOB9Bo0"


def main():
    # this step is for initialization of the authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # toy example to get started
    text_query = 'COVID'
    count = 3
    try:
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.search_tweets, lang="en", q=text_query).items(count)

        # Pulling information from tweets iterable object
        tweets_list = [tweet.text for tweet in tweets]

        for tweet in tweets_list:
            print(tweet)

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)


if __name__ == "__main__":
    main()