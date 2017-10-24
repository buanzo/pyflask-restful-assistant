import imp
import os

from pprint import pprint


class FAXPluginBase(type):
    plugins = []

    def __init__(cls, name, bases, attrs):
        if name != 'FAXPlugin':
            FAXPluginBase.plugins.append(cls)

    @classmethod
    def prettyPrint(cls):
        print("+{:-<19}+{:-<56}+".format('', ''))
        print("| {:^17} | {:^54} |".format("Plugin Name", "Description"))
        print("+{:-<19}+{:-<56}+".format('', ''))
        for plugin in FAXPluginBase.plugins:
            n = plugin.__name__
            d = plugin.description
            if plugin.default:
                n = '{}*'.format(n)
            print("| {:17} | {:54} |".format(n, d))
        print("+{:-<19}+{:-<56}+".format('', ''))
        print("Note: A plugin marked with * runs by default.\n")


class FAXPlugin(object, metaclass=FAXPluginBase):
    author = 'Arturo Busleiman <buanzo@buanzo.com.ar>'
    description = 'FAXPlugin is the class Plugins will base on'
    default = False

    def __init__(self, name=None, default=False):
        self.name = name


def load_plugins(dirs):
    for dir in dirs:
        for filename in os.listdir(dir):
            modname, ext = os.path.splitext(filename)
            if ext == '.py':
                file, path, descr = imp.find_module(modname, [dir])
                if file:
                    mod = imp.load_module(modname, file, path, descr)
    return FAXPluginBase.plugins
