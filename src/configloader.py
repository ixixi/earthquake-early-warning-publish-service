#! /usr/bin/env python
# -*- coding: utf-8 -*-

config_dir = '../conf/'

class JSONLoader:
    def load_json(self,fname, encoding='utf-8'):
        if os.path.isfile(fname):
            with open(fname) as f:
                return json.load(f, encoding)
        return {}

