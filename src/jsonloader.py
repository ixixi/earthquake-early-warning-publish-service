#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

class JSONLoader:
    @classmethod
    def load_json(self,fname, encoding='utf-8'):
        if os.path.isfile(fname):
            with open(fname) as f:
                return json.load(f, encoding)
        return {}

