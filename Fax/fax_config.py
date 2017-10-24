#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Arturo 'Buanzo' Busleiman

import os
import configparser
from Fax.fax_util import FAXUtil
from pprint import pprint
import pdb

""" FAXConfig class initializes with a configuration file,
and provides access to configuration variables. """


class FAXConfig():
    pluginsdir = None
    templatesdir = None

    @classmethod
    def update(cls):
        FAXConfig.pluginsdir = FAXConfig.get_plugins_path()
        FAXConfig.templatesdir = FAXConfig.get_templates_path()

    @classmethod
    def get_plugins_path(cls):
        scriptdir = os.path.dirname(__file__)
        path = os.path.join(scriptdir, 'plugins')
        return(path)

    @classmethod
    def get_templates_path(cls):
        scriptdir = os.path.dirname(__file__)
        path = os.path.join(scriptdir, 'templates')
        return(path)

    def __init__(self, configFile=None):
        if configFile is None:
            return None
        self.parser = configparser.ConfigParser()
        if len(self.parser.read(configFile)) == 0:
            raise IOError

        # This is the actual absolute minimum for fax.conf:
        if not self.parser.has_section('global'):
            raise NameError
        self.sections = self.parser.sections()
        self.options = self.parser.options

        reqoptions = ('author', 'basename', 'backname',
                      'backname_services', 'output_dir')
        for option in reqoptions:
            if option not in self.parser['global']:
                raise NameError

        FAXConfig.update()

    def config(self):
        sections = self.sections
        options = self.options
        retObj = {'sections': sections}
        for section in sections:
            retObj[section] = {}
            for option in options(section):
                data = self.parser.get(section, option)
                if len(data.split(',')) > 1:
                    data = data.replace(' ', '')
                    data = data.split(',')
                retObj[section][option] = data
        return(retObj)

    def validateFeatures(self):
        okList = []
        errorList = []
        features = self.config()['global']['features']
        for feature in features.split(','):
            cleaned = feature.strip()
            if FAXUtil.validFeatureName(cleaned):
                okList.append(cleaned)
            else:
                errorList.append(cleaned)
        retObj = {'valid': okList,
                  'invalid': errorList}
        return(retObj)

if __name__ == "__main__":
    cfg = FAXConfig(configFile='/home/buanzo/buanzo/git/pyflask-restful-assistant/frasspy.conf')
    cfg.validateFeatures()
    pprint(cfg.config())
    print("This file is not to be called directly.")
