#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
from tweepy import OAuthHandler, Stream, StreamListener, TweepError, API
from amqp.amqpclient import AMQPClient
from telopmessage import TelopMessage
import logging
import urllib 
import re
import json
import traceback

consumer_key    = '{fill in your consumer_key}'
consumer_secret = '{fill in your consumer_secret}'
access_key      = '{fill in your access key}'
access_secret   = '{fill in your access secret}'

my_screen_name = '{fill in your screen name}'

level_user_mst = {
                 'eew_jp'          : 'error',
                 'earthquake_jp'   : 'warn',
                 my_screen_name    : 'warn',
                 'other'           : 'info'}

level_tweet_mst = {
                 'timeline'        : 'info',
                 'mention'         : 'error',
                 'conversation'    : 'debug',
                 'retweet'         : 'debug'}

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
    
    __amqp_client = AMQPClient()
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
    stream = UserStream(auth, CustomeStreamListener(api=API(auth_handler=auth)))
    stream.timeout = None
    stream.user_stream()

        
if __name__ == '__main__':
	main()

def daemon_process():
    print 'daemon start!'
    main()
