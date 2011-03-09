#!/usr/bin/env python

import tweepy
import time
import sys, codecs
import os
import datetime
import webbrowser

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

INTERVAL = 60 * 5
FILE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_home_timeline(api):
    latest_id = None
    while True:
        latest_timeline = api.home_timeline(count=200, since_id=latest_id)
        latest_id = latest_timeline[0].id
        # print latest_timeline in INTERVAL seconds
        sleep_time = INTERVAL / len(latest_timeline)
        for tweet in latest_timeline:
            sys.stdout.write("@%s:: %s\n" % (tweet.author.screen_name,
                                             tweet.text.replace("\n", " ")))
            sys.stdout.flush()
            time.sleep(sleep_time)

def main():
    """
    Consumer key: TdrgpiHH3rEvijxEiSgFg
Consumer secret: 5RLZj4HNCoLXdyip9kJbiZvZrVgLGs10mrZXfTvHE
Verification pin number from twitter.com: 1743897"""
    consumer_key = "TdrgpiHH3rEvijxEiSgFg"
    consumer_secret = "5RLZj4HNCoLXdyip9kJbiZvZrVgLGs10mrZXfTvHE"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    pin_file = os.path.join(FILE_DIR, "twitter_pin")
    if os.path.exists(pin_file):
        f = open(pin_file, "r")
        strs = f.readlines()
        access_key = strs[0][:-1]
        access_secret = strs[1]
        f.close()
    else:
        webbrowser.open(auth.get_authorization_url())
        pin = raw_input('Verification pin number from twitter.com: ').strip()
        token = auth.get_access_token(verifier=pin)
        f = open(pin_file, "w")
        f.write(token.key + "\n")
        f.write(token.secret)
        f.close()
        access_key = token.key
        access_secret = token.secret
    while True:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        try:
            run_home_timeline(api)
        except tweepy.TweepError, e:
            time.sleep(60)      # wait 60 seconds
            sys.stdout.write("cannot connect! @ "
                             + str(datetime.datetime.today())
                             + "\n")
            sys.stdout.flush()
            pass                # back to top
    
if __name__ == "__main__":
  main()
