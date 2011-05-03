#!/usr/bin/env python
# -*- coding: utf-8 -*-
from amqplib import client_0_8 as amqp
import json

class TelopMessage(object):
    __message_body = 'default message'
    __data_type = 'twitter.timeline'
    __level = 'error'
    __raw_json = None
    
    def __init__(self, message_body=None,data_type=None,level=None,raw_json=None):
        self.__message_body = message_body
        self.__data_type = data_type
        self.__level = level
        self.__raw_json = raw_json

    def hook(self,obj):
        if isinstance(obj, TelopMessage):
            return obj.__dict__
        else:
            return obj