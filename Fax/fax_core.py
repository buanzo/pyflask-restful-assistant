#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Arturo 'Buanzo' Busleiman

import os
import sys

from pathlib import Path
from pprint import pprint

from Fax.fax_util import FAXUtil
from Fax.fax_config import FAXConfig
from Fax.fax_plugin import FAXPluginBase


class FAXCore():
    PRE_WRITE_HOOKS = ('dependencyCheck', 'setupVars', 'getImportLine',
                       'render', 'filter',)
    POST_WRITE_HOOKS = ('afterWrite',)
    checkOnly = False
    faxConfig = None
    templatesPath = None
    status = []
    importLines = []
    renderObjects = []
    configDeps = []

    def __init__(self, cfgPath=None, templatesPath=None, checkOnly=False):
        try:
            FAXCore.faxConfig = FAXConfig(configFile=cfgPath)
        except:
            raise IOError

        if FAXCore.faxConfig is None:  # This should not happen
            print("Config file not specified. Use  --config.")
            sys.exit(1)

        FAXCore.checkOnly = checkOnly
        if checkOnly is False:
            self.preWriteHooksToRun = FAXCore.PRE_WRITE_HOOKS
            self.postWriteHooksToRun = FAXCore.POST_WRITE_HOOKS
        else:
            self.preWriteHooksToRun = ('dependencyCheck',)
            self.postWriteHooksToRun = ('',)

    """ This function takes the list of required features
    off the configuration file, and verifies the plugins exist.
    returns: True or False
    status: TODO
    """
    def checkFeatures(self):
        wanted = FAXCore.faxConfig.validateFeatures()
        if len(wanted['invalid']) > 0:
            ifl = ', '.join(wanted['invalid'])
            print('fax: Invalid features requested: {}'.ifl)
            sys.exit(3)
        if len(wanted['valid']) > 0:
            return(wanted['valid'])
        else:
            print('fax: requested features are invalid. Check your fax.conf.')
            sys.exit(4)

    """ Check if config['global']['output_dir'] exists and is a directory.
    """
    def checkOutputDir(self):
        od = Path(FAXCore.faxConfig.config()['global']['output_dir'])
        if od.exists() and od.is_dir():
            return True
        return False

    def config(self):
        return(FAXCore.faxConfig.config())

    """ main() is indeed main().
        it gets plugins, and might get more stuff
        TODO: it needs to:
        * collect declarative data off plugins
        * resolve execution and plugin requirements
        * update the FAXCore status class attribute
    """
    def main(self, plugins=None):
        plugins = [P() for P in plugins]
        default_plugins = []

        # Populate the list of plugins that run by default
        for plugin in plugins:
            dft = getattr(plugin, 'default')
            pname = getattr(plugin, 'name').lower()
            if dft is True:
                default_plugins.append(pname)

        # Run all hooks, in order, on every plugin
        for hook in self.preWriteHooksToRun:
            for plugin in plugins:
                if hasattr(plugin, hook):
                    pname = getattr(plugin, 'name').lower()
                    try:
                        reqfeatures = self.config()['global']['features']
                    except:
                        reqfeatures = default_plugins
                    if pname in reqfeatures or pname in default_plugins:
                        # print("Executing {} on {}".format(hook, plugin))
                        getattr(plugin, hook)()

        # Show any statuses reported by plugins
        if len(FAXCore.status) > 0:
            print("fax: Plugins reported these messages:")
            pprint(FAXCore.status)

        # Now, work on the renderObjects we got
        for renderObj in FAXCore.renderObjects:
            getattr(renderObj, 'write')()

        # Finally, run any post-write hooks:
        for hook in self.postWriteHooksToRun:
            for plugin in plugins:
                if hasattr(plugin, hook):
                    pname = getattr(plugin, 'name').lower()
                    if pname in reqfeatures or pname in default_plugins:
                        getattr(plugin, hook)()

if __name__ == "__main__":
    print("This file is not to be called directly.")
