#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
from tweepy import OAuthHandler, Stream, StreamListener, TweepError, API
from amqp.amqpclient import AMQPClient
from telopmessage import TelopMessage
from jsonloader import JSONLoader
import logging
import urllib 
import re
import json
import traceback


CONFIG_DIR = '../conf/'
CONFIG_TWITTER    = CONFIG_DIR + 'twitter.conf'
CONFIG_HANDLE_MST = CONFIG_DIR + 'handle_mst.conf'
CONFIG_AMQP       = CONFIG_DIR + 'amqp.conf'

print 'load twitter conf'
twitter_conf = JSONLoader.load_json(CONFIG_TWITTER)

consumer_key    = twitter_conf['consumer_key'] 
consumer_secret = twitter_conf['consumer_secret'] 
access_key      = twitter_conf['access_key']
access_secret   = twitter_conf['access_secret']
my_screen_name  = twitter_conf['my_screen_name']

print 'load handle-mst conf'
handle_mst_conf = JSONLoader.load_json(CONFIG_HANDLE_MST)

level_tweet_mst = handle_mst_conf['level_tweet_mst']
level_user_mst  = handle_mst_conf['level_user_mst']

print 'load amqp conf'
amqp_conf     = JSONLoader.load_json(CONFIG_AMQP)
amqp_userid   = amqp_conf['user_id']
amqp_password = amqp_conf['password']
amqp_host     = amqp_conf['host']
amqp_exchange = amqp_conf['default_exchange']


def get_oauth():
     
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    
    return auth
 
class UserStream(Stream): 
    
    def user_stream(self, follow=None, track=None, async=False, locations=None):
        """
        Twitter User Streamを開く
        """
        self.parameters = {"delimited": "length", }
        self.headers['Content-type'] = "application/x-www-form-urlencoded"
        if self.running:
            raise TweepError('Stream object already connected!')
        self.scheme = "https"
        self.host = 'userstream.twitter.com'
        self.url = '/2/user.json'
        self.body = urllib.urlencode(self.parameters)
        self._start(async)
 
class CustomeStreamListener(StreamListener):
    
    __amqp_client = None
    __raw_data = None
    __json_data = None
    
    def on_data(self, data):
        self.__raw_data = data
        print 'on_data'
        super(self.__class__,self).on_data(data)
     
    def on_status(self, status):
        self.__json_data = json.loads(self.__raw_data)
        """
        ステータス取得時のイベントハンドラ
        """
        if hasattr(status, "text" ):
            print 'author' + ' : ' + str(status.author)
            print 'created_at(datetime)' + ' : ' + str(status.created_at)
            print 'entitiest' + ' : ' + str(status.entities)
            print 'favorite' + ' : ' + str(status.favorite)
            print 'favorited' + ' : ' + str(status.favorited)
            print 'id' + ' : ' + str(status.id)
            print 'id_str' + ' : ' + str(status.id_str)
            print 'user' + ' : ' + str(status.user)
            print 'user.screen_name' + ' : ' + str(status.user.screen_name)
            
            data_type = 'timeline'
            level = level_user_mst['other']

            # memtionは無条件でレベルを設定
            if status.text.find('@'+my_screen_name) >= 0:
                data_type = 'mention'
            # 自分が絡まない会話のレベルは下げる
            elif status.in_reply_to_screen_name and status.in_reply_to_screen_name != my_screen_name:
                data_type = 'conversation'
            # RTのレベルは下げる
            elif status.text.find('RT @') >= 0:
                data_type = 'retweet'
            
            level = level_tweet_mst[data_type]
            
            # ユーザ指定でレベルを(あれば)付与
            if status.user.screen_name in level_user_mst:
                level = level_user_mst[status.user.screen_name]
            
            message_body = self.build_message_body(status)
            
            level = level.encode('utf-8')

            print '[%s] (%s) : %s' % (level,data_type,message_body)

            telop_message = TelopMessage(message_body=message_body,data_type=data_type,level=level,raw_json=self.__raw_data)
            serialized_message = json.dumps(telop_message,indent=2, default=telop_message.hook)
            
            try:
                self.__amqp_client.push(serialized_message)
            except :
                print 'Error!'
                print serialized_message
                traceback.print_exc()

        else:
            # TODO:favとかretweetedとかfollowの通知上げるか?
            print status
            
    def set_amqp_client(self,amqp_client):
        self.__amqp_client = amqp_client

    def build_message_body(self,status):
        raw_text = status.text
        screen_name = status.user.screen_name
        text = self.filter(raw_text)
        message_body = '%s: %s' % (screen_name,text)
        return message_body
        
    url_re = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    hashtag_re = re.compile('TODO')
    def filter(self,text):
        text = self.url_re.sub('{url}',text.encode('utf-8'))
        return text
    
    eew_re = re.compile( u'(の地震が発生しました|です|される最大震度は)')
    def _shorten(self,message):
        message = message.split('http')[0]
        message = self.eew_re.sub('',message)
        message = message.replace(u'マグニチュード','M')
        message = message[10:]
        return message.encode('utf-8')

def main():
    auth = get_oauth()
    amqp_client = AMQPClient(amqp_host,amqp_userid,amqp_password,amqp_exchange)
    csl = CustomeStreamListener(api=API(auth_handler=auth))
    csl.set_amqp_client(amqp_client)
    stream = UserStream(auth,csl)
    stream.timeout = None
    stream.user_stream()

        
if __name__ == '__main__':
    main()

def daemon_process():
    print 'daemon start!'
    main()
