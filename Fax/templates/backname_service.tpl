#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: {{names.author}}

from flask_restful import Resource


class {{names.backname|upper}}_{{servicename|capitalize}}(Resource):
    def __init__(self):
        """
        Class Initialization.
        """
        pass

    def get(self,{{parameters}}):
        """
        GET method handler for {{names.backname|upper}}__{{names.servicename|capitalize}}
        """
        pass

    def post(self,{{parameters}}):
        """
        POST method handler for {{names.backname|upper}}__{{names.servicename|capitalize}}
        """
        pass

    def delete(self,{{parameters}}):
        """
        DELETE method handler for {{names.backname|upper}}__{{names.servicename|capitalize}}
        """
        pass

    def put(self,{{parameters}}):
        """
        PUT method handler for {{names.backname|upper}}__{{names.servicename|capitalize}}
        """
        pass


if __name__ == '__main__':
    print("{{names.servicename|capitalize}}")

