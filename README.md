Earthquake-Early-Warning publish service (eew-pub)
===========

This service(eew-pub) publish messages of earthquake-early-waning to a RabbitMQ exchange.
To get messages of earthquake-early-warning, eew-pub uses Twitter User Streaming API.
So eew-pub achieve Real-time publishing.

If you have *'Degital Telopper EN-NL1068'*, you are lucky.
Using *'Digital Telopper Subscribe Client'*, **you can watch TV ovarlapping with Earthquake-Early-Warning telops** (like captions).

 * [Degital Telopper EN-NL1068](http://entis-marketing.jp/products/dt/nl1068/index.html)
 * [Digital Telopper SubScribe Client](https://github.com/ixixi/digitaltelopper-subscribe-client)

## Getting Started

### install

#### install the language processor

* [python(2.6 or later)](http://www.python.org/getit/)

#### install dependencies

 *  [py-amqplib](http://code.google.com/p/py-amqplib/)
 *  [tweepy](https://github.com/joshthecoder/tweepy)
 *  [python-daemon](http://pypi.python.org/pypi/python-daemon/)

#### install earthquake-early-warning-publish-service

$ git clone https://github.com/ixixi/earthquake-early-warning-publish-service.git

### configure

$ cd eathquake-early-warning-publish-service  
$ vim conf/amqp.conf  
 - write RabbitMQ connection settings  
$ vim conf/twitter.conf  
 - write your consumer key/secret, access token/secret and screen name.  

### run

$ sh twitter_userstream_start.sh
