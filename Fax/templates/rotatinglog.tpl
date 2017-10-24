d
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: {{names.author}}

import logging
from os import getpid
from socket import SOCK_STREAM, SOCK_DGRAM
from logging.handlers import RotatingFileHandler, SysLogHandler
from pprint import pprint

"""This file implements a Syslog class that supports logging
to text files, in a rotating manner. Other plugins implement,
remote and and standard local syslog.
"""

class {{names.basename|upper}}RotatingSyslog():
    """Provides convenient methods to configure
       and log messages via standard unix local
       or remote syslog or classic logfile with rotation."""

    def __init__(self, initmsg=None, name='{{names.basename|upper}}',
                 logdir='{{params.logdir}}'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.msgprefix = '{}[{}]: '.format(name, getpid())

        lsh = RotatingFileHandler(logdir, mode='a',
                                  maxBytes={{params.maxbytes}},
                                  backupCount={{params.count}},
                                  encoding='utf-8',
                                  delay=False)

        self.logger.addHandler(lsh)

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
    s = {{names.basename|upper}}RotatingSyslog()
    s.info('INFO-PRIORITY-MESSAGE')
    s.warning('INFO-WARNING-MESSAGE')
    s.error('INFO-ERROR-MESSAGE')
    s.debug('INFO-DEBUG-MESSAGE')
