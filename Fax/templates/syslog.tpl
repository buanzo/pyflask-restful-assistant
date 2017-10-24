d
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: {{names.author}}

import logging
from os import getpid
from socket import SOCK_STREAM, SOCK_DGRAM
from logging.handlers import RotatingFileHandler, SysLogHandler
from pprint import pprint

"""This file implements a Syslog class that supports standard
local syslog. Other plugins implement, 'logrotated' file-logging,
and sending to a remote syslog server.
"""

class {{names.basename|upper}}Syslog():
    """Provides convenient methods to configure
       and log messages via standard unix local
       or remote syslog or classic logfile with rotation."""

    def __init__(self, initmsg=None, name='{{names.basename|upper}}'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.msgprefix = '{}[{}]: '.format(name, getpid())

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
    s = {{names.basename|upper}}Syslog()
    s.info('INFO-PRIORITY-MESSAGE')
    s.warning('INFO-WARNING-MESSAGE')
    s.error('INFO-ERROR-MESSAGE')
    s.debug('INFO-DEBUG-MESSAGE')
