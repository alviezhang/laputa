# coding: utf-8


from laputa.fetch import Fetcher
from laputa.parse import CardParser

__all__ = ['WeiboUser']


PAGE_SIZE = 10
WEIBO_URL = 'http://m.weibo.cn/page/json'
CONTAINER_PREFIX = '100505'


FETCH_TYPE = {
    'follows': {
        'container_type': 'FOLLOWERS',
        'text': '关注'
    },
    'posts': {
        'container_type': 'WEIBO_SECOND_PROFILE_WEIBO',
        'text': '微博'
    },
    'fans': {
        'container_type': 'FANS',
        'text': '粉丝'
    },
    'likes': {
        'container_type': 'WEIBO_SECOND_PROFILE_LIKE_WEIBO',
        'text': '赞过的微博'
    },
}


class WeiboUser:
    def __init__(self, uid):
        self.uid = uid
        self._fetcher = Fetcher()

    def _build_fetch_url(self, fetch_type, page=1):
        if fetch_type in FETCH_TYPE:
            fetch_type = FETCH_TYPE[fetch_type]['container_type']
        else:
            raise RuntimeError('type {} not supported'.format(fetch_type))

        fetch_url = "{url}?containerid={prefix}{uid}_-_{type}&page={page}"
        params = {
            'url': WEIBO_URL,
            'prefix': CONTAINER_PREFIX,
            'uid': self.uid,
            'type': fetch_type,
            'page': page,
        }
        return fetch_url.format(**params)

    def get(self, fetch_type, size=PAGE_SIZE, page=1, after=[]):
        card_list = []
        page = 1
        until = list(after)
        while True:
            fetch_url = self._build_fetch_url(fetch_type, page)
            result = self._fetcher.fetch(fetch_url)
            cards = self._result_handler(result)
            if len(cards) == 0:
                break
            for card in cards:
                if card.id in until:
                    return card_list
                card_list.append(card)
                if len(card_list) == size:
                    return card_list
            page += 1
        return card_list

    def _result_handler(self, result):
        return CardParser.parse(result)
