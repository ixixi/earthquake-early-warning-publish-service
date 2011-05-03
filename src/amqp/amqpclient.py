#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011/04/30

@author: ixixi
'''
from amqplib import client_0_8 as amqp

userId = 'guest'
password = 'guest'
host = 'ec2-175-41-210-68.ap-northeast-1.compute.amazonaws.com'

'''
userId   = '{fill in RabbitMQ userId }'
password = '{fill in RabbitMQ password }'
host     = '{fill in RabbitMQ server}'
'''

DEFAULT_EXCHANGE = 'fanoutexchange'

class AMQPClient:
    
    connection = None
    channel = None
    exchange = None
    
    def __init__(self,exchange=DEFAULT_EXCHANGE):
        self.connection = amqp.Connection(host, userid=userId, password=password, ssl=False)
        self.channel = self.connection.channel()
        self.channel.access_request('/data', active=True, write=True)
        self.channel.exchange_declare(exchange, 'fanout', auto_delete=True)
        self.exchange=exchange
        
    def push(self,message_body):
        message = amqp.Message(message_body, content_type='application/json')
        self.channel.basic_publish(message,self.exchange)
        print 'pushed'
    
    def pop(self):
        return None
