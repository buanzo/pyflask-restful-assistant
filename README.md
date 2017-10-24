pyflask-api-generator (also known as Fax - Flask API eXtrapolator)
------------------------------------------------------------------

# Introduction

pyflask-api-generator is a plugin-based tool that generates Python 3 source code
for the main purpose of implement RESTful API server applications using the
Flask-RESTful module. It is built using Python 3.5, Jinja2 templating library
and other standard Python modules.

The alias name for this tool is 'fax' (Flask-Api-eXtrapolator, if I may).

# Usage

Fax includes command line switches to specify a different configuration file,
listing included plugins and their description, show plugin config-file dependencies,
and Dumping the configuration to screen. The --version argument also shows which
paths will be read to find template files and plugins.

Of course, because of Python's ConfigParser module, -h / --help is available:

```
pyflask-api-generator $ ./fax -h
>>> pyflask-api-generator aka frasspy <<<
usage: fax [-h] [-c CONFIG] [--version] [-l] [-n] [-D]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file path (/home/buanzo/buanzo/git/pyflask-
                        restful-assistant/frasspy.conf)
  --version             Show version and paths
  -l, --list            List available plugins
  -n, --needs           Run dependency check on plugins and report back
  -D, --dump            Dumps configuration
```

## Listing Plugins

```
pyflask-api-generator $ ./fax -l
>>> pyflask-api-generator aka fax <<<
+-------------------+--------------------------------------------------------+
|    Plugin Name    |                      Description                       |
+-------------------+--------------------------------------------------------+
| EntryPoint*       | Creates primary Flask-RESTful entrypoint.              |
| PEP8Check*        | Filter plugin that runs pep8 validation                |
| RemoteSyslog      | Adds remote syslog support to your application         |
| RotatingLog       | Adds rotated logging to your application               |
| Package*          | Creates empty __init__.py inside package folder        |
| Syslog            | Adds local syslog support to your application          |
| DBTools           | Adds MySQL support to your application                 |
| Services*         | Creates flask-restful code for each defined service    |
| SamplePlugin      | Sample plugin. Read it if you want to code your own.   |
+-------------------+--------------------------------------------------------+
Note: A plugin marked with * runs by default.
```

## Version and Template/Plugin Paths

```
pyflask-api-generator $ ./fax --version
>>> pyflask-api-generator aka fax <<<
version: 0.1.0
Templates Path : /opt/pyflask-api-generator/Fax/plugins
Plugins Path   : /opt/pyflask-api-generator/Fax/templates
```

## Plugin Dependencies

When using the -n switch, only those plugins that would run (by default or by
setting features= on the config file) will output dependency data:


```
pyflask-api-generator $ ./fax -n
>>> pyflask-api-generator aka fax <<<
EntryPoint needs basename in global
EntryPoint needs privname in global
EntryPoint needs backname in global
EntryPoint needs author in global
EntryPoint needs backname_services in global
EntryPoint needs paths in service1
EntryPoint needs paths in service2
EntryPoint needs paths in anotherservice
RemoteSyslog needs basename in global
RemoteSyslog needs author in global
Package needs author in global
Package needs basename in global
DBTools needs basename in global
DBTools needs author in global
DBTools needs user in dbtools
DBTools needs pass in dbtools
DBTools needs host in dbtools
DBTools needs db in dbtools
DBTools needs user in dbtools_readonly
DBTools needs pass in dbtools_readonly
DBTools needs host in dbtools_readonly
DBTools needs db in dbtools_readonly
Services needs author in global
Services needs basename in global
Services needs backname in global
Services needs backname_services in global
```

# Configuration File

Fax reads a configuration file (by default, fax.conf in the current working directory).
You can specify a different configuration file by using the "-c" command-line switch.

This is how a Fax configuration file looks like:

```
[global]
author = Sample Author <sampleauthor@company.mail>
basename = app
privname = internal
features = remotesyslog, dbtools
backname = api
backname_services = users,config,help
# MUST exist. FAX only creates inside it:
output_dir = /usr/local/src/my_api_server

[users]
paths = /service1/<someparam>,/service1/<someparam>/<someid>

[config]
paths = /service2/<id>

[help]
paths = /icanusewhateveriwant/<id>,/evendifferent/structs/<id>

[dbtools]
user = rwUser
pass = rwPassword
host = rwHostname
db = rwDatabase

[dbtools_readonly]
user = roUser
pass = roPassword
host = roHostname
db = roDatabase

[remotesyslog]
url=tcp://host:port
initmsg="My-Api-Server has started"
```

## Configuration Dump

```
pyflask-api-generator $ ./fax -D
>>> pyflask-api-generator aka fax <<<
{'anotherservice': {'paths': ['/icanusewhateveriwant/<id>',
                              '/evendifferent/structs/<id>']},
 'dbtools': {'db': 'rwDatabase',
             'host': 'rwHostname',
             'pass': 'rwPassword',
             'user': 'rwUser'},
 'dbtools_readonly': {'db': 'roDatabase',
                      'host': 'roHostname',
                      'pass': 'roPassword',
                      'user': 'roUser'},
 'global': {'author': 'Some Author <SomeAuthoro@somecompany>',
            'backname': 'api',
            'backname_services': ['service1', 'service2', 'anotherservice'],
            'basename': 'example',
            'features': ['dbtools', 'remotesyslog'],
            'output_dir': '/tmp/api',
            'privname': 'privname'},
 'remotesyslog': {'initmsg': '"test remote syslog message sent during syslog '
                             'class __init__"',
                  'url': 'tcp://host:port'},
 'rotatinglog': {'count': '10',
                 'logdir': '/some/log/location',
                 'maxsize': '1048576'},
 'sections': ['global',
              'service1',
              'service2',
              'anotherservice',
              'dbtools',
              'dbtools_readonly',
              'syslog',
              'remotesyslog',
              'rotatinglog'],
 'service1': {'paths': ['/service1/<someparam>',
                        '/service1/<someparam>/<someid>']},
 'service2': {'paths': '/service2/<id>'},
 'syslog': {'initmsg': '"test syslog message sent on syslog class __init__"'}}
```

# Structure of Plugins

## Database support plugin

```python
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
```

## PEP8 compliance check plugin

```python
# PEP8Check plugin
from Fax.fax_plugin import FAXPlugin
from Fax.plugin_api import PluginApi, FAXRender
import pep8

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

```


# Useful Links

* http://jinja.pocoo.org/docs/2.9/
* http://jinja.pocoo.org/docs/2.9/templates/
* ConfigParser https://docs.python.org/3.6/library/configparser.html
* https://docs.python.org/3/library/tokenize.html
