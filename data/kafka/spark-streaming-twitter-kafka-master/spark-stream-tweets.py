#!/usr/bin/env python

from __future__ import print_function

import sys
import json

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def get_people_with_hashtags(tweet):
    """
    Returns (people, hashtags) if successful, otherwise returns empty tuple. All users
    except author have an @ sign appended to the front.
    """
    data = json.loads(tweet)
    try:
        hashtags = ["#" + hashtag["text"] for hashtag in data['entities']['hashtags']]
        # Tweets without hashtags are a waste of time
        if len(hashtags) == 0:
            return ()
        author = data['user']['screen_name']
        mentions = ["@" + user["screen_name"] for user in data['entities']['user_mentions']]
        people = mentions + [author]
        return (people, hashtags)
    except KeyError:
        return ()

def filter_out_unicode(x):
    """
    Pass in a list of (authors, hashtags) and return a list of hashtags that are not unicode
    """
    hashtags = []
    for hashtag in x[1]:
        try:
            hashtags.append(str(hashtag))
        except UnicodeEncodeError:
            pass
    return (x[0], hashtags)

def flatten(x):
    """
    Input:
    ([people],[hashtags]).

    Output:
    [(hashtag, (main_author_flag, {person})),
     ...]
    """
    all_combinations = []

    people = x[0]
    hashtags = x[1]

    for person in people:
        for hashtag in hashtags:
            main_author_flag = 0 if "@" in person else 1
            all_combinations.append((hashtag, (main_author_flag, {person})))
    
    return all_combinations 


if __name__ == "__main__":
    zkQuorum = "localhost:2181"
    topic = "twitter-stream"

    # User-supplied command arguments
    if len(sys.argv) != 3:
        print("Usage: spark-stream-tweets.py <min_hashtag_counts> <seconds_to_run>")
        exit(-1)
    min_hashtag_counts = int(sys.argv[1])
    seconds_to_run = int(sys.argv[2])

    sc = SparkContext("local[2]", appName="TwitterStreamKafka")
    ssc = StreamingContext(sc, seconds_to_run)

    tweets = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    # Tweet processing. 
    # Kafka passes a tuple of message ID and message text. Message text is the tweet text.
    # All tweets are turned into ([people],[hashtags]) and tweets without hashtags are filtered
    # out.

    # Returns ([people], [hashtags])
    lines = tweets.map(lambda x: get_people_with_hashtags(x[1])).filter(lambda x: len(x)>0)

    # Filters out unicode hashtags
    hashtags = lines.map(filter_out_unicode)

    # Make all possible combinations --> (hashtag, (main_author, {person})), where main_author == 1
    # if it is the tweet author
    flat_hashtags = hashtags.flatMap(flatten)

    # Reduce by hashtag key into a list of authors and a count of tweets.
    hash_tag_authors_and_counts = flat_hashtags.reduceByKey(lambda a, b: (a[0] + b[0], a[1] | b[1]))

    # Only keep hashtags with more than a certain number of values
    top_hashtags = hash_tag_authors_and_counts.filter(lambda x: x[1][0] >= min_hashtag_counts)

    top_hashtags.pprint()

    ssc.start()
    ssc.awaitTermination()

