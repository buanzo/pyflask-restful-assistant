#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: {{author_name}}


from flask import Flask, request
from flask_restful import Api, Resource

"""This is a comment.
   Yes. Very nice.
"""

{% for import_line in import_lines %}
{{import_line}}
{% endfor %}


#
# INITIALIZATION
#
{{names.basename|lower}}_app = Flask(__name__)
api = Api({{names.basename|lower}}_app)

#
# API Routing
#

{% for service in paths %}
api.add_resource({{names.backname|upper}}_{{service|capitalize}},
{% for path in paths[service] %}
                 '{{path}}',
{% endfor %}
                 )

{% endfor %}

if __name__ == '__main__':
    {{names.basename|lower}}_app.run(host='127.0.0.1', debug=True)
    # Remember to cleanup here [dbClose(), etc, etc]

