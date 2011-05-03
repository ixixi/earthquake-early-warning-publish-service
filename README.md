MessagePack
===========
Extremely efficient object serialization library. It's like JSON, but very fast and small.


## What's MessagePack?

MessagePack is a binary-based efficient object serialization library. It enables to exchange structured objects between many languages like JSON. But unlike JSON, it is very fast and small.

Typical small integer (like flags or error code) is saved only in 1 byte, and typical short string only needs 1 byte except the length of the string itself. \[1,2,3\] (3 elements array) is serialized in 4 bytes using MessagePack as follows:

    require 'msgpack'
    msg = [1,2,3].to_msgpack  #=> "\x93\x01\x02\x03"
    MessagePack.unpack(msg)   #=> [1,2,3]


## Performance

![Serialization + Deserialization Speed Test](http://msgpack.sourceforge.net/index/speedtest.png)

In this test, it measured the elapsed time of serializing and deserializing 200,000 target objects. The target object consists of the three integers and 512 bytes string.
The source code of this test is available from [frsyuki' serializer-speed-test repository.](http://github.com/frsyuki/serializer-speed-test)


## Getting Started

Usage and other documents about implementations in each language are found at [the web site.](http://msgpack.sourceforge.net/)


## Learn More

  - [Project Web Site](http://msgpack.sourceforge.net/)
  - [MessagePack format specification](http://msgpack.sourceforge.net/spec)
  - [Repository at github](http://github.com/msgpack/msgpack)
  - [Wiki](http://msgpack.sourceforge.net/start)
  - [MessagePack-RPC](http://github.com/msgpack/msgpack-rpc)




Earthquake-Early-Warning publish service (eew-pub)
===========
This service(eew-pub) publish messages of earthquake-early-waning to a RabbitMQ exchange.
To get messages of earthquake-early-warning, eew-pub uses Twitter User Streaming API.
So eew-pub achieve Real-time publishing.

If you have '(Degital Telopper EN-NL1068)[http://entis-marketing.jp/products/dt/nl1068/index.html]', you are lucky.
Using 'DigitalTelopper Subscribe Client', you can watch TV ovarlapping with Earthquake-Early-Warning telops (like captions).

 - (DigitalTelopper SubScribe Client)[https://github.com/ixixi/digitaltelopper-subscribe-client]
## Getting Started

install the language processor
 - (python(2.6 or later))[http://www.python.org/getit/]
install dependencies
 - (py-amqplib)[http://entis-marketing.jp/products/dt/nl1068/index.html]
 - (tweepy)[https://github.com/joshthecoder/tweepy]
 - (python-daemon)[http://pypi.python.org/pypi/python-daemon/]

$ git clone https://github.com/ixixi/earthquake-early-warning-publish-service.git
$ cd eathquake-early-warning-publish-service
$ vim amqp.conf
 - write RabbitMQ connection settings
$ vim twitter.conf
 - write your consumer key/secret, access token/secret and screen name.
$ sh twitter_userstream_start.sh

