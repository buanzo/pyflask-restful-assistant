#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: {{names.author}}

import logging
from os import getpid
from socket import SOCK_STREAM, SOCK_DGRAM
from logging.handlers import RotatingFileHandler, SysLogHandler
from pprint import pprint

"""This file implements a Syslog class that supports logging
to a remote syslog server. Other plugins implement, logrotated
file-logging, and standard local syslog.
"""

class {{names.basename|upper}}RemoteSyslog():
    """Provides convenient methods to configure
       and log messages via standard unix local
       or remote syslog or classic logfile with rotation."""

    def __init__(self, initmsg=None, name='{{names.basename|lower}}',
                 host='{{params.host}}', port={{params.port}},
                 tcp={{params.tcp}}):
        self.logger = logging.getLogger(name)
        self.port = port
        self.logger.setLevel(logging.DEBUG)
        self.msgprefix = '{}[{}]: '.format(name, getpid())

        if tcp is False:
            t = 'udp'
            sockettype = SOCK_DGRAM
        else:
            t = 'tcp'
            sockettype = SOCK_STREAM

        rsh = SysLogHandler(address=(host, self.port),
                            facility=SysLogHandler.LOG_DAEMON,
                            socktype=sockettype)
        self.logger.addHandler(rsh)
        self.info("logging to {}://{}:{}".format(t, host, port))

        if initmsg is not None:
            self.info('{}'.format(initmsg))

    def info(self, msg):
        """Sends msg to syslog with LOG_INFO priority."""
        self.logger.info('{} {}'.format(self.msgprefix, msg))

    def warning(self, msg):
        """Sends msg to syslog with LOG_WARNING priority."""
        self.logger.warning('{} {}'.format(self.msgprefix, msg))

    def error(self, msg):
        """Sends msg to syslog with LOG_ERR priority."""
        self.logger.error('{} {}'.format(self.msgprefix, msg))

    def debug(self, msg):
        """Sends msg to syslog with LOG_DEBUG priority."""
        self.logger.debug('{} {}'.format(self.msgprefix, msg))

if __name__ == '__main__':
    s = {{names.basename|upper}}RemoteSyslog()
    s.info('INFO-PRIORITY-MESSAGE')
    s.warning('INFO-WARNING-MESSAGE')
    s.error('INFO-ERROR-MESSAGE')
    s.debug('INFO-DEBUG-MESSAGE')
