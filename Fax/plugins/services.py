from Fax.fax_plugin import FAXPlugin
from Fax.plugin_api import PluginApi, FAXRender

import re
import sys
import json
from pprint import pprint


class Services(FAXPlugin):
    author = 'Arturo Busleiman <buanzo@buanzo.com.ar>'
    description = 'Creates flask-restful code for each defined service'
    default = True

    def __init__(self):
        self.name = self.__class__.__name__
        self.api = PluginApi(callerName=self.name)
        self.cfg = self.api.config()

    def dependencyCheck(self):
        # This hook checks if self.cfg holds whatever
        # values we need. Config should have already been
        # validated at a basic level at this point
        # by FAXCore/FAXConfig.
        #
        # good place to create plugin-wide template vars
        # although most plugins build their templatevars
        # on the render hook
        #
        self.reqitems = ('author', 'basename', 'backname', 'backname_services')
        for item in self.reqitems:
            self.api.report_config_dependency('global', item)
        for service in self.cfg['global']['backname_services']:
            self.api.report_config_dependency(service, 'paths')
        return

    def setupVars(self):
        self.names = {}
        for item in self.reqitems:
            self.names[item] = self.cfg['global'][item]
        self.templatevars = {}
        self.templatevars['names'] = self.names
        # NOTE: This plugin creates multiple files
        # and for that reason, some templatevars
        # will be set on render()

    def getImportLine(self):
        # This function returns a string
        # that represents the python code to import the
        # generated module.
        # e.g 'from blah_dbtools import BLAHDb'
        # It is used by entrypoint plugin.
        # TODO: actually implement all this
        # example: from fapi.cp1fw_nftables import CP1FW_Nftables
        #          from t1.t2 import t3
        #          t1 = basename.lower()
        #          t2 = backname.lower()_service.lower()
        #          t3 = backname.upper()_service.capitalize()
        t1 = self.names['basename'].lower()   # fapi
        b = self.names['backname'].lower()  # cp1fw
        services = self.names['backname_services']   # nftables
        for s in services:
            t1 = self.names['basename'].lower()
            t2 = '{}_{}'.format(b, s)
            t3 = '{}_{}'.format(b.upper(), s.capitalize())
            rs = 'from {}.{} import {}'.format(t1, t2, t3)
            self.api.report_import_line(rs)
        return(None)

    def paramhelper(self, service):
        params = []
        rex = re.compile('\<\w+\>')
        paths = self.cfg[service]['paths']
        if isinstance(paths, list):
            paths = ''.join(paths)
        for path in paths.split(','):
            pp = rex.findall(path)
            for p in pp:
                p = p.replace('<', '').replace('>', '=None')
                if p not in params:
                    params.append(p)
        s = ', '.join(params)
        return(" {}".format(s))

    def render(self):
        t1 = self.names['basename'].lower()   # fapi
        b = self.names['backname'].lower()  # cp1fw
        # TODO: move to setupVars
        services = self.names['backname_services']   # nftables
        for s in services:
            self.templatevars['servicename'] = s
            self.templatevars['parameters'] = self.paramhelper(s)
            t1 = self.names['basename'].lower()
            path = '{}/'.format(t1)
            fn = '{}_{}.py'.format(b, s)
            output = self.api.render(template='backname_service.tpl',
                                     variables=self.templatevars)
            retObj = FAXRender(creator=self.name,
                               relpath=path,
                               filename=fn,
                               contents=output)
            self.api.report_render_object(retObj)
        return(None)
