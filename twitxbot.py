import os
import sys
import re
import tweepy
import json
import urllib
import random
user_name = 'bill'      #user who will get reply from our bot
bot_name  = 'zuckXbot'  #our bot_name
flag = False
def xkcd():
    global flag
    img_url = json.loads(urllib.urlopen("http://xkcd.com/%d/info.0.json"%(random.randint(1,1690))).read())["img"];
    urllib.urlretrieve("%s"%(img_url),'tweetimg.jpg')
    flag = True
    return '#XKCD'

def chuck_norris_jokes():
    return json.loads(urllib.urlopen("http://api.icndb.com/jokes/random?").read())["value"]["joke"]

def bill_meme():
    global user_name,flag
    urllib.urlretrieve('http://belikebill.azurewebsites.net/billgen-API.php?default=1&name=%s'%(user_name),'tweetimg.jpg' )
    flag = True
    return '#BeLike%s'%(user_name)

CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

#Status Object Contents
"""
mentions = api.mentions_timeline()
print json.dumps(mentions[0]._json, sort_keys=True, indent=4)

{ 
    "created_at": "Sat Jun 11 10:21:42 +0000 2016", 
    "entities": {
        "hashtags": [],  
        "symbols": [], 
        "urls": [], 
        "user_mentions": [
            {
                "id": 741518031822544901, 
                "id_str": "741518031822544901", 
                "indices": [
                    0, 
                    9
                ], 
                "name": "zuckbot", 
                "screen_name": "zuckXbot"
            }
        ]
    }, 
     
    "favorite_count": 0, 
    "favorited": false, 
    "geo": null, 
    "id": 741576132793794561,  
    "in_reply_to_screen_name": "zuckXbot", 
    "in_reply_to_status_id": null, 
    "in_reply_to_user_id": 741518031822544901, 
    "is_quote_status": false, 
    "lang": "en", 
    "place": null,  
    "retweet_count": 0, 
    "retweeted": false, 
    "source": "<a href=\"http://corebird.baedert.org\" rel=\"nofollow\">Corebird</a>", 
    "text": "@zuckXbot bot testing one two three...? https://t.co/MwS226PSgA", 
    "truncated": false, 
    
    "user": {
        "created_at": "Wed Dec 30 11:33:10 +0000 2009", 
        "favourites_count": 58, 
        "follow_request_sent": false, 
        "followers_count": 32, 
        "following": false, 
        "friends_count": 112, 
        "geo_enabled": true, 
        "has_extended_profile": true, 
        "id": 100475149, 
        "lang": "en", 
        "listed_count": 5, 
        "location": "/dev/null", 
        "name": "zuck_007",  
        "protected": false, 
        "screen_name": "zuck_007", 
        "statuses_count": 904, 
        "time_zone": "New Delhi", 
        "url": "https://t.co/L7v8s97Wn6", 
        "utc_offset": 19800, 
        "verified": false
    }
}

"""
def main():
    global user_name,bot_name,flag
    mentions = api.mentions_timeline()
    for post in mentions:
        user_name = post._json["user"]["screen_name"]
        bot_name = post._json["in_reply_to_screen_name"]
        if post.favorited == False and user_name != bot_name:
            post_id = post.id
            print post_id,user_name,post.text
            if bot_name == user_name:
                continue
            if flag:
                os.system('rm tweetimg.jpg')
                flag = False
            ch = random.randint(1,3)
            if ch == 1:
                put_post = xkcd()
            elif ch == 2:
                put_post = bill_meme()
            else:
                put_post = chuck_norris_jokes()
            
            reply_post = "@%s %s"%(user_name,put_post)
            
            if put_post[0] != "#":
                api.update_status(reply_post[:140],post_id)
            else:
                api.update_with_media('./tweetimg.jpg',reply_post[:140],post_id)
            api.create_favorite(post_id)    

if __name__ == '__main__':
    main()
