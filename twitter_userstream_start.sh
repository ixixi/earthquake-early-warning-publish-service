#/usr/bin/sh
cd src
nohup python twitteruserstream.py >> ../log/tw_user_stream.log 2>> ../log/tw_user_stream_err.log &
#python twitteruserstream.py
