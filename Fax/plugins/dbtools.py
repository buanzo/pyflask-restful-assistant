from Fax.fax_plugin import FAXPlugin
from Fax.plugin_api import PluginApi, FAXRender

import sys


class DBTools(FAXPlugin):
    author = 'Arturo Busleiman <buanzo@buanzo.com.ar>'
    description = 'Adds MySQL support to your application'

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
        #
        # TODO: error-control this for proper fax exit()
        self.api.report_config_dependency('global', 'basename')
        self.api.report_config_dependency(section='global',
                                          option='author')
        reqoptions = ('user', 'pass', 'host', 'db')
        reqsections = ('dbtools', 'dbtools_readonly')
        for section in reqsections:
            for option in reqoptions:
                self.api.report_config_dependency(section, option)

    def setupVars(self):
        """ This hook is run after dependencyCheck for the purposes
        of setting up any variables that might be required for other
        hooks, particularly by the render() hook.
        """
        self.names = {}
        self.templatevars = {}
        self.names['basename'] = self.cfg['global']['basename']
        self.dbtools = {}
        self.dbtools['user'] = self.cfg['dbtools']['user']
        self.dbtools['pass'] = self.cfg['dbtools']['pass']
        self.dbtools['host'] = self.cfg['dbtools']['host']
        self.dbtools['db'] = self.cfg['dbtools']['db']
        self.dbtools_ro = {}
        self.dbtools_ro['user'] = self.cfg['dbtools_readonly']['user']
        self.dbtools_ro['pass'] = self.cfg['dbtools_readonly']['pass']
        self.dbtools_ro['host'] = self.cfg['dbtools_readonly']['host']
        self.dbtools_ro['db'] = self.cfg['dbtools_readonly']['db']
        self.templatevars['names'] = self.names
        self.templatevars['dbtools'] = self.dbtools
        self.templatevars['dbtools_readonly'] = self.dbtools_ro
        self.templatevars['author_name'] = self.cfg['global']['author']
        return

    def getImportLine(self):
        # This function returns a string
        # that represents the python code to import the
        # generated module.
        # e.g 'from blah_dbtools import BLAHDb'
        # It is used by entrypoint plugin.
        # TODO: actually implement all this
        # example: from cuac_dbtools import CUACDb
        l = self.names['basename'].lower()
        u = l.upper()
        rs = 'from {}.{}_dbtools import {}Db'.format(l, l, u)
        self.api.report_import_line(rs)
        return(rs)

    def render(self):
        # First, we create our own variables, adapted
        # for template readability
        lb = self.names['basename'].lower()
        vars = self.templatevars
        path = '{}/'.format(lb)
        fn = '{}_dbtools.py'.format(lb)
        output = self.api.render(template='dbtools.tpl',
                                 variables=vars)
        retObj = FAXRender(creator=self.name,
                           relpath=path,
                           filename=fn,
                           contents=output)
        self.api.report_render_object(retObj)
        return(retObj)
