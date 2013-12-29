#! /usr/bin/env python
#coding:utf-8
import simplejson as json
import time
import sys
import oauth2 as oauth
import signal
from urllib import urlencode
from colorama import Fore, Back, Style

consumerKey   ='your consumer key'
consumerSecret='yout consumer Secret'
accessToken   ='your access token'
accessSecret  ='your access secret'

def getTimeLine(num):
    TL_URL='https://api.twitter.com/1.1/statuses/home_timeline.json'
    resp, content=client.request(TL_URL+'?count='+str(num),'GET')
    if resp.status != 200:
        print "TwitterError!"
        dat="[]"
    else:
        dat=json.loads(content)
    return dat

def getFavo(num):
    TL_URL='https://api.twitter.com/1.1/favorites/list.json'
    resp, content=client.request(TL_URL+'?count='+str(num),'GET')
    if resp.status != 200:
        print "TwitterError!"
        dat="[]"
    else:
        dat=json.loads(content)
    return dat

def post_tweet(text):
    POST_URL='https://api.twitter.com/1.1/statuses/update.json'
    client.request(POST_URL,'POST',urlencode({'status': unicode(text).encode('utf-8')   }),)     

def print_tweet(user,id,text,case):
    if case=="l":
        print Fore.GREEN,Style.BRIGHT
    else:
        print Fore.GREEN,Style.BRIGHT,
    print(user+"@"+id+" ~%"+Fore.RESET+text.replace('\n', ' '))

def print_Timeline(dat,case):
    for i in range(0,len(dat)):
        print_tweet(
            tl_data[i]['user']['name'],tl_data[i]['user']['screen_name'],tl_data[i]['text'].replace('\n', ' ')
            ,case)

def print_detail(op):
    print('Invalid option  -'+op)
    print('-p  text                        textをtwitterに投稿')
    print('-al number                      numberの数だけTLを取得')
    print('-a  number                      numberの数だけTLを取得(詰めて表示)')
    print('-fl number                      numberの数だけふぁぼを取得')
    print('-f  number                      numberの数だけふぁぼを取得(詰めて表示)')


if __name__=="__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    argvs = sys.argv  
    argc = len(argvs) 
    client  = oauth.Client(
        oauth.Consumer(key=consumerKey, secret=consumerSecret),oauth.Token(accessToken, accessSecret))
    if argc == 1: 
        while(1):
            tl_data=getTimeLine(10)
            print_Timeline(tl_data,"l")
            time.sleep(10)
    elif argc == 3:
        if   argvs[1] ==  "-p":
            post_tweet(argvs[2])
        elif argvs[1] ==  "-f":
            tl_data=getFavo(argvs[2])
            print_Timeline(tl_data,"s")
        elif argvs[1] ==  "-fl":
            tl_data=getFavo(argvs[2])
            print_Timeline(tl_data,"l")
        elif argvs[1] ==  "-al":
            tl_data=getTimeLine(argvs[2])
            print_Timeline(tl_data,"l")
        elif argvs[1] ==  "-a":
            tl_data=getTimeLine(argvs[2])
            print_Timeline(tl_data,"s")
        else:
            print_detail(argvs[1])
    else:
        print_detail(argvs[1])
