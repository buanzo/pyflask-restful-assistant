from Fax.fax_plugin import FAXPlugin
from Fax.plugin_api import PluginApi, FAXRender

from pprint import pprint

""" A FAXPlugin returns multiple FAXRender objects.
    Each object represents the contents of a file
    to be created below cfg['global']['output_dir'].
    Plugins have config file dependencies.
    The dependencyCheck() method of each plugin is
    called by FAXCore to determine what is up.
    Plugins are allowed to stop execution
    via sys.exit().
"""


class EntryPoint(FAXPlugin):
    author = 'Arturo Busleiman <buanzo@buanzo.com.ar>'
    description = 'Creates primary Flask-RESTful entrypoint.'
    default = True

    def __init__(self):
        self.name = self.__class__.__name__
        self.api = PluginApi(callerName=self.name)
        self.cfg = self.api.config()

    def getImportLine(self):
        # EntryPoint does not require an import string
        # TODO: test the None return
        return(None)

    def dependencyCheck(self):
        # This hook checks if self.cfg holds whatever
        # values we need.
        # PluginApi() offers report_config_dependency() for this
        # more complicated needs might require the plugin
        # author to print an error message and sys.exit()
        self.api.report_config_dependency('global', 'basename')
        self.api.report_config_dependency('global', 'privname')
        self.api.report_config_dependency('global', 'backname')
        self.api.report_config_dependency('global', 'author')
        self.api.report_config_dependency('global', 'backname_services')
        for service in self.cfg['global']['backname_services']:
            self.api.report_config_dependency(service, 'paths')
        return

    def setupVars(self):
        self.vars = {}
        self.vars['author_name'] = self.cfg['global']['author']
        self.vars['services'] = self.cfg['global']['backname_services']
        paths = {}
        names = {}
        for service in self.vars['services']:
            if isinstance(self.cfg[service]['paths'], str):
                paths[service] = [self.cfg[service]['paths']]
            else:
                paths[service] = self.cfg[service]['paths']

        self.vars['paths'] = paths
        names['basename'] = self.cfg['global']['basename']
        names['privname'] = self.cfg['global']['privname']
        names['backname'] = self.cfg['global']['backname']
        self.vars['names'] = names
        self.vars['import_lines'] = self.api.get_import_lines()

    def render(self):
        # print("This is hook render() at {}".format(self.name))
        # First, we create our own variables, adapted
        # for template readability

        fn = '{}.py'.format(self.vars['names']['basename'].lower())
        pprint(self.vars['import_lines'])

        output = self.api.render(template='entrypoint.tpl',
                                 variables=self.vars)

        retObj = FAXRender(creator=self.name,
                           filename=fn,
                           contents=output)
        self.api.report_render_object(retObj)
        return(retObj)
