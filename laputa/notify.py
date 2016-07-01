# coding: utf-8

import requests


_IFTTT_URL = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'


class IFTTTNotifier:
    def __init__(self, key, event_name):
        self._key = key
        self._timeout = 5
        self._event = event_name

    def trigger(self, **kwargs):
        return self._trigger(self._event, **kwargs)

    def _trigger(self, event, **kwargs):
        url = _IFTTT_URL.format(key=self._key, event=event)
        valid_params = ('value1', 'value2', 'value3')
        query_data = {}
        for key in valid_params:
            if key in kwargs:
                query_data[key] = kwargs[key]
        if query_data:
            r = requests.post(url, json=query_data, timeout=self._timeout)
        else:
            r = requests.post(url, timeout=self._timeout)
        if r.status_code == 200:
            print(r.text)
        elif r.status_code == 401:
            raise RuntimeError('IFTTT trigger failed! invalid key')
        else:
            raise RuntimeError('IFTTT trigger failed! unknow error')
