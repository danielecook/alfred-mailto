#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2013 deanishe@deanishe.net.
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2013-12-04
#

"""
"""

from __future__ import print_function, unicode_literals

import os
import json

import alfred


class Settings(dict):

    log_path = os.path.join(alfred.work(True), u'debug.log')
    settings_path = os.path.join(alfred.work(False), u'settings.json')
    logging_default = False  # logging off by default

    default_settings = {
        "default_app": None,
        "clients": [],
        "use_name": None,
        "logging": logging_default
    }

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        self._nosave = False
        if not os.path.exists(self.settings_path):
            for key, val in self.default_settings.items():
                self[key] = val
            self._save()  # save default settings
        else:
            self._load()

    def _load(self):
        self._nosave = True
        with open(self.settings_path, 'rb') as file:
            for key, value in json.load(file).items():
                self[key] = value
        self._nosave = False

    def _save(self):
        if self._nosave:
            return
        data = {}
        for key, value in self.items():
            data[key] = value
        with open(self.settings_path, 'wb') as file:
            json.dump(data, file, sort_keys=True, indent=2, encoding='utf-8')

    # dict methods
    def __setitem__(self, key, value):
        super(Settings, self).__setitem__(key, value)
        self._save()

    def update(self, *args, **kwargs):
        super(Settings, self).update(*args, **kwargs)
        self._save()

    def setdefault(self, key, value=None):
        super(Settings, self).setdefault(key, value)
        self._save()
