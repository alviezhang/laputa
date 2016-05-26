#coding: utf-8

import requests
import logging


logger = logging.getLogger(__name__)


class Fetcher:
    def __init__(self):
        pass

    def fetch(self, url):
        logger.info('fetching: {}'.format(url))
        response = requests.get(url)
        return response.text

