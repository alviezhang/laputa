#coding: utf-8


import logging
import simplejson as json

from bs4 import BeautifulSoup
from datetime import datetime


WEIBO_DOMAIN = 'http://m.weibo.cn'


def convert_text(text):
    converted = BeautifulSoup(text, 'html.parser').get_text()
    return converted


class CardParser:
    @classmethod
    def parse(cls, response):
        data = json.loads(response)
        logging.debug('ok: {}, cards count: {}'.format(data['ok'], data['count']))
        card_list = []
        if data['count'] and int(data['count']) > 0:
            mod = data['cards'][0]
            if mod['mod_type'] == 'mod/pagelist':
                card_list = cls._parse_page(mod['card_group'])
            elif mod['mod_type'] == 'mod/empty':
                pass
            else:
                logging.warn('unknow mod_type: {}'.format(mod['card_group']))
        return card_list

    @classmethod
    def _parse_page(cls, card_group):
        card_list = []
        for raw_card in card_group:
            card = None
            if raw_card['card_type'] == 9:
                card = Post(raw_card['mblog'])
            elif raw_card['card_type'] == 10:
                card = User(raw_card['user'])
            else:
                logging.warn('unknow card type: {}'.format(raw_card['card_type']))
            if card:
                card_list.append(card)
        return card_list


class Card:
    pass


class Post(Card):
    def __init__(self, post):
        self.create_time = datetime.fromtimestamp(post['created_timestamp'])
        self.id = post['id']
        self.bid = post['bid']
        self.uid = post['user']['id']
        self.retweeted = False

        text = convert_text(post['text'])
        if 'retweeted_status' in post:
            origin_card = post['retweeted_status']
            origin_text = convert_text(origin_card['text'])
            origin_user = origin_card['user']['screen_name']
            text = '{}: @{}: {}'.format(text, origin_user, origin_text)
            self.retweeted = True

        self.text = text

    @property
    def url(self):
        params = {
            'uid': self.uid,
            'bid': self.bid,
        }
        return '{}/{uid}/{bid}'.format(WEIBO_DOMAIN,**params)

    def __str__(self):
        return '{}: {}..'.format(type(self), self.text[:8])


class User(Card):
    def __init__(self, user):
        self.id = user['id']
        self.name = user['screen_name']
        self.profile_url = user['profile_url']
        self.profile_image_url = user['profile_image_url']
        self.gender = user['gender']

    def __str__(self):
        return '{}: {}..'.format(type(self), self.name[:8])

