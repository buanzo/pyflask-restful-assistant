#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Arturo 'Buanzo' Busleiman

import os
import sys
from pathlib import Path

from Fax.fax_config import FAXConfig
from Fax.fax_core import FAXCore

from pprint import pprint

# TODO: MAYBE move the jinja functionality to its own class?
from jinja2 import Environment, FileSystemLoader


class PluginApi():

    def __init__(self, callerName=None):
        if callerName is None:
            # Pyblack magic to get caller name out of ModuleSpec
            # We will issue a status message so the operator
            # can tell which plugin is lacking the parameter
            # I might remove this black magic code
            for f in sys._current_frames().values():
                x = f.f_back.f_globals['__spec__']
                self.callerName = str(x).split('name=')[1] \
                                        .split(',')[0] \
                                        .replace("'", "")
                self.report_status('PluginApi lacks callerName parameter')
                del f
                del x
                break
        else:
            self.callerName = callerName

    @classmethod
    def config(cls):
        return (FAXCore.faxConfig.config())

    def report_render_object(self, o):
        FAXCore.renderObjects.append(o)

    def report_import_line(self, s):
        FAXCore.importLines.append(s)

    def report_config_dependency(self, section=None, option=None):
        if section is None or option is None:
            print("{}: report_config_dependency() lacks required parameters".
                  format(self.callerName))
            sys.exit(50)

        if FAXCore.checkOnly is True:
            print("{} needs {} in {}".format(self.callerName, option, section))

        if option not in self.config()[section]:
            print("fax: No '{}' option in '[{}]', required by {}".format(
                  option, section, self.callerName))
            if FAXCore.checkOnly is False:
                # Immediate exit only on full runs (i.e no --needs)
                sys.exit(51)

        cObj = {}
        cObj['plugin'] = self.callerName
        cObj['section'] = section
        cObj['option'] = option
        FAXCore.configDeps.append(cObj)

    def report_status(self, s):
        # VERY GENERIC NOW, comes off plugin config requirements.
        # Requirements can be complex, hence no PluginApi
        # method for actual checking, but for reporting only
        # PluginApi.report_missing_config() should be
        # used for non-critical missing config parameters
        # Critical parameters should raise sys.exit(255) by plugin.
        # Period.
        sObj = {}
        sObj['plugin'] = self.callerName
        sObj['status'] = s
        FAXCore.status.append(sObj)

    def get_render_objects(self):
        return(FAXCore.renderObjects)

    def get_import_lines(self):
        return(FAXCore.importLines)

    def get_status(self):
        return(FAXCore.status)

    def replace_render_objects(self, filteredObjects):
        FAXCore.renderObjects = filteredObjects

    def render(self, template=None, variables=None):
        if template is None or variables is None:
            return(False)  # TODO: enhance error ret
        if FAXConfig.templatesdir is None:
            return(False)

        tp = os.path.join(FAXConfig.templatesdir, template)
        loader = FileSystemLoader(FAXConfig.templatesdir)
        j2_env = Environment(loader=loader,
                             trim_blocks=True)
        x = j2_env.get_template(template).render(variables)
        return(x)

""" FAXRender objects are returned by plugin render() methods.
    It returns the rendered text as __str__()
    It has a write() method for obvious reasons.
    It can also run diff() against the existing file contents.
"""


class FAXRender():
    def __init__(self, creator, filename, contents, relpath=''):
        self.outputdir = PluginApi.config()['global']['output_dir']
        self.relpath = relpath
        self.contents = contents
        self.filename = filename
        self.creator = creator
        self.path = os.path.join(self.outputdir,
                                 self.relpath)
        self.fullpath = os.path.join(self.path,
                                     self.filename)

    def __str__(self):
        return(self.contents)

    def write(self):
        fp = Path(self.path)
        if not fp.is_dir():
            print("fax: creating {}".format(self.path))
        try:
            fp.mkdir(parents=True, exist_ok=True)
        except:
            print("fax: cannot create {}".format(self.path))
            sys.exit(29)

        print("fax: writing to {}".format(self.fullpath))
        fn = Path(self.fullpath)
        try:
            fn.write_text(self.contents)
        except:
            print("fax: error creating/writing to {}".format(self.fullpath))
            sys.exit(30)

    def replaceContents(self, newContents):
        self.contents = newContents

    def diff(self):
        # TODO: compares existing self.path contents
        # against self.contents
        pass
