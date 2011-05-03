#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import daemon
from daemon.daemon import DaemonContext
from twitteruserstream import daemon_process
import sys

#pidfile = PIDLockFile("/var/run/daemontest.pid")
dc = DaemonContext(
#                  pidfile=pidfile,
#                  stdout=open('telopper_daemon_out.log', 'w+'),
#                  stderr=open('telopper_daemon_err.log', 'w+')
                    stdout = sys.stdout,
                    stderr = sys.stderr)
with dc:
    print "hello "
    daemon_process()
