from Fax.fax_plugin import FAXPlugin
from Fax.plugin_api import PluginApi, FAXRender
from pprint import pprint


class SamplePlugin(FAXPlugin):
    author = 'Arturo Busleiman <buanzo@buanzo.com.ar>'
    description = 'Sample plugin. Read it if you want to code your own.'
    default = False

    def __init__(self):
        self.name = self.__class__.__name__
        self.api = PluginApi(callerName=self.name)
        self.cfg = self.api.config()

    def getImportLine(self):
        s = 'from someblah import someBlah'
        return(None)

    def dependencyCheck(self):
        # This hook checks if self.cfg holds whatever
        # values we need. Config should have already been
        # validated at a basic level at this point
        # by FAXCore/FAXConfig.
        #
        # Returns (True/False,'optional message')
        #
        # self.api.report_config_dependency('somesection','someoption')
        pass

    def setupVars(self):
        # This hook is run post-dependencyCheck
        # Variables that are required by render()
        # are created here, inside self.
        pass

    def render(self):
        # First, we create our own variables, adapted
        # for template readability
        # vars = {}
        # vars['author_name'] = self.cfg['global']['author']

        # lb = self.cfg['global']['basename'].lower()
        # path = '{}/'.format(lb)
        # fn = '__init__.py'

        # output = self.api.render(template='package.tpl',
        #                         variables=vars)

        # retObj = FAXRender(creator=self.name,
        #                   relpath=path,
        #                   filename=fn,
        #                   contents=output)
        # self.api.report_render_object(retObj)
        pass

    def filter(self):
        # This hook is called after render hook.
        # We can get all the FAXRender objects the other
        # plugins reported to fax_core.
        # rObjs = self.api.get_render_objects()
        # We could modify those objects, for any reason.
        # for obj in rObjs:
        #    if obj.creator is "DBTools":
        #        obj.contents = "fuck you dbtools"
        # self.api.replace_render_objects(rObjs)
        pass
