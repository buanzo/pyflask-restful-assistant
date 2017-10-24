from Fax.fax_plugin import FAXPlugin
from Fax.plugin_api import PluginApi, FAXRender


class Package(FAXPlugin):
    author = 'Arturo Busleiman <buanzo@buanzo.com.ar>'
    description = 'Creates empty __init__.py inside package folder'
    default = True

    def __init__(self):
        self.name = self.__class__.__name__
        self.api = PluginApi(callerName=self.name)
        self.cfg = self.api.config()

    def getImportLine(self):
        return(None)

    def dependencyCheck(self):
        # This hook checks if self.cfg holds whatever
        # values we need. Config should have already been
        # validated at a basic level at this point
        # by FAXCore/FAXConfig.
        #
        # Returns (True/False,'optional message')
        #
        self.api.report_config_dependency('global', 'author')
        self.api.report_config_dependency('global', 'basename')
        return

    def setupVars(self):
        self.vars = {}
        self.vars['author_name'] = self.cfg['global']['author']
        self.vars['basename'] = self.cfg['global']['basename']

    def render(self):
        # print("This is hook render() at {}".format(self.name))
        # First, we create our own variables, adapted
        # for template readability

        lb = self.vars['basename'].lower()
        path = '{}/'.format(lb)
        fn = '__init__.py'

        output = self.api.render(template='package.tpl',
                                 variables=self.vars)

        retObj = FAXRender(creator=self.name,
                           relpath=path,
                           filename=fn,
                           contents=output)
        self.api.report_render_object(retObj)
        return(retObj)
