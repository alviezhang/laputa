# coding: utf-8

import os
import toml


class Recorder:
    def __init__(self, file_name):
        self.file_name = file_name
        self.config = {
            'posts': [],
            'fans': 0,
            'likes': [],
            'follows': 0,
        }

    def _update_config(self, config):
        for key in self.config.keys():
            if key in config:
                self.config[key] = config[key]

    def read(self):
        if os.path.exists(self.file_name) and os.path.isfile(self.file_name):
            with open(self.file_name) as config_file:
                config = toml.loads(config_file.read())
                self._update_config(config)
        return self.config

    def write(self, config):
        self._update_config(config)
        with open(self.file_name, 'w') as config_file:
            config_str = toml.dumps(self.config)
            config_file.write(config_str)
