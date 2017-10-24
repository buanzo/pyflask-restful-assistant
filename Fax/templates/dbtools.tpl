#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: {{author_name}}

import mysql.connector
import json

""" This file implements the {{names.basename|lower}}Db class
"""


class {{names.basename|upper}}Db():
    """Class initialization."""
    def __init__(self):
        self.config = {
            'user': '{{dbtools.user}}',
            'password': '{{dbtools.pass}}',
            'host': '{{dbtools.host}}',
            'database': '{{dbtools.db}}',
        }
        self.readonlyConfig = {
            'user': '{{dbtools_readonly.user}}',
            'password': '{{dbtools_readonly.pass}}',
            'host': '{{dbtools_readonly.host}}',
            'database': '{{dbtools_readonly.db}}',
        }
        self.dbconn = mysql.connector.connect(**self.config)
        self.readonly_dbconn = mysql.connector.connect(
                                    **self.readonlyConfig, autocommit=True)

    """Close mysql connections"""
    def dbClose(self):
        self.dbconn.close()
        self.readonly_dbconn.close()

    """Obtain a db cursor, reconnect if needed
       The readonly parameter is True by default"""
    def getDbCursor(self, readonly=True):
        # Assign dbconn according to desired connection level (RO/RW)
        if readonly is False:
            dbconn = self.dbconn
        else:
            dbconn = self.readonly_dbconn
        dbconn.ping(reconnect=True, attempts=5, delay=1)
        try:
            cursor = dbconn.cursor()
        except:
            dbconn.reconnect(attempts=5, delay=1)
        finally:
            if dbconn.is_connected():
                cursor = dbconn.cursor()
            else:
                return(None)
        return(cursor)

