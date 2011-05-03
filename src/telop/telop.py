#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
push Digital Telopper EN-NL1068
@see
http://www.entis-marketing.jp/products/dt/nl1068/index.html

Created on 2011/04/29

@author: ixixi
'''

import urllib

COLOR_CODE = {'white':0,'red':1,'green':2,'blue':3}

INFO_COLOR = 'blue'
WARN_COLOR = 'green'
ERROR_COLOR = 'red'

class Telopper:
    
    __telopper_ip = None
    __telopper_url = None
    __default_color = None
    
    def __init__(self,ip):
        self.set_ip(ip)
        pass
    
    def set_ip(self,ip):
        self.__telopper_ip =ip
        self.__telopper_url = 'http://' + self.__telopper_ip + '/user.cgi'
        
    def set_default_color(self,color):
        self.__default_color = color
        
    def post_telop(self,message,color=__default_color,speed=None,row=None,left=None):
        postdata = {}
        postdata['data'] = ' ' + message + ' '
        if color: postdata['color'] = COLOR_CODE[color]
        if speed: postdata['speed'] = speed           #無視されるっぽい?
        if row: postdata['row'] = row
        if left: postdata['left'] = left
        params = urllib.urlencode(postdata)
        #print self.__telopper_url + '?' + params
        try:
            urllib.urlopen(self.__telopper_url + '?' + params)
        except Exception:                   #正常時もExceptionが出るので仕方なく
            pass
        
    def post_info(self,message,color=INFO_COLOR,speed=None,row=None,left=None):
        self.post_telop(message,color,speed,row,left)

    def post_warn(self,message,color=WARN_COLOR,speed=None,row=None,left=None):
        self.post_telop(message,color,speed,row,left)

    def post_error(self,message,color=ERROR_COLOR,speed=None,row=None,left=None,count=1):
        for var in range(0, count):
            self.post_telop(message,color,speed,row,left)
        
