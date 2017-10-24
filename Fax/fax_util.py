#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Arturo 'Buanzo' Busleiman

import re


class FAXUtil():
    @classmethod
    def validFeatureName(self, value):
        if not re.match("^[a-zA-Z_]{1,16}$", value):
            return False
        return True


if __name__ == "__main__":
    print("This file is not to be called directly.")
