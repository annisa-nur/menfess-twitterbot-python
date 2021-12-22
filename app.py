# from flask import Flask
from twitter import Twitter
from async_upload import *
import requests
import twitter
import time
import constants
from datetime import timezone
import tweepy
import logging

tw = Twitter()

# app = Flask(__name__)
# @app.route("/", methods = ['GET', 'POST'])
def start():
    print("Starting program...")
    dms = list()
    while True:
        if len(dms) is not 0 :
            for i in range(len(dms)):
                message = dms[i]['message']
                print('================')
                print(f'len message = ', {len(message)})
                print('================')
                # I take sender_id just in case you want to know who's sent the message
                sender_id = dms[i]['sender_id']
                id = dms[i]['id']
                
                if constants.trigger in message.lower():
                    ## MULTIPLE TWEET WITH NO MEDIA AND WITH MEDIA
                    if len(message) > 280 :
                        posted = 0
                        complete = 0
                        # if constants.trigger in message.lower():
                        a = True
                        while (a):
                            if len(message) is not 0:
                                if dms[i]['media'] is None:
                                    leftcheck = 260
                                    left = 0
                                    right = 280
                                    check = message[leftcheck:right].split(' ')
                                    separator = len(check[-1]) ## kasih separator biar diakhir tweet engga ada kata terpenggal, kalo terpenggal di masukin ke next tweet.
                                    message1 = message[left:right-separator] # + '(cont..)'
                        
                                    ## API RELOAD ##
                                    auth = tweepy.OAuthHandler(constants.CONSUMER_KEY, constants.CONSUMER_SCRET)
                                    auth.set_access_token(constants.ACCESS_KEY, constants.ACCESS_SECRET)
                                    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
                                     ## API RELOAD ##

                                    if complete == 0:
                                        try:
                                            sendtwt = api.update_status(message1)
                                            time.sleep(10)
                                            print('build the first one...')
                                        except Exception as e:
                                            print(e)
                                            time.sleep(10)
                                            pass

                                        posted += 1
                                        complete = sendtwt.id
                                        message = message[right-separator:len(message)]
                                        postid = complete
                                        rttime = sendtwt.created_at.replace(tzinfo=timezone.utc)                         
                        
                                    else: 
                                        try :
                                            complete = api.update_status(message1, in_reply_to_status_id = complete, auto_populate_reply_metadata = True).id
                                            time.sleep(10)
                                            message = message[right-separator:len(message)]
                                            print('still doing till finish...')
                                        except Exception as e:
                                            print(e)
                                            time.sleep(30)
                                            pass
                                    
                                else:
                                    print('Message with >280 char can not attach media (photo/video)')
                                    tw.delete_dm(id)
                                    dms = list()

                            else:
                                a = False
                                print(f'isi message akhir: ', message)
                                print('Thread is successfuly uploaded..') 
                                tw.delete_dm(id)
                                dms = list()
                     
                
                ## SINGLE TWEET WITH NO MEDIA OR WITH MEDIA
                    if len(message) > 0 and len(message) <= 280:
                            if len(message) is not 0: 
                                    if dms[i]['media'] is None:
                                        print("DM will be posted")
                                        tw.post_single_tweet(message)
                                        tw.delete_dm(id)
                                    else:
                                        print("DM will be posted with media")
                                        print(dms[i]['shorted_media_url'])
                                        tw.post_single_tweet_with_media(message, dms[i]['media'],dms[i]['shorted_media_url'], dms[i]['type'])
                                        if dms[i]['media_data'] == 'photo' or dms[i]['media_data'] == 'video':
                                            tw.delete_dm(id)
                                        else:
                                            pass
                            else:
                                print("DM deleted because its empty..")
                                tw.delete_dm(id)

                else:
                    print("DM will be deleted because does not contains keyword..")
                    tw.delete_dm(id)


            dms = list()

        else:
            dms = tw.read_dm()
            if len(dms) is 0 or dms is None:
                ## pengaturan selang waktu tweet disini, kalkulasiin sama fungsi delete di module twitter
                time.sleep(90)

if __name__ == "__main__":
    # port = 3000
    # app.run(host = '0.0.0.0', port = port)
    start()