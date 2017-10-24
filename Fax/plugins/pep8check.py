from Fax.fax_plugin import FAXPlugin
from Fax.plugin_api import PluginApi, FAXRender
import pep8
from pprint import pprint


class PEP8Check(FAXPlugin):
    author = 'Arturo Busleiman <buanzo@buanzo.com.ar>'
    description = 'Filter plugin that runs pep8 validation'
    default = True

    def __init__(self):
        self.name = self.__class__.__name__
        self.api = PluginApi(callerName=self.name)

    def afterWrite(self):
        pep8style = pep8.StyleGuide(quiet=False)
        objs = self.api.get_render_objects()
        f2c = []
        for obj in objs:
            f2c.append(obj.fullpath)
        result = pep8style.check_files(f2c)
