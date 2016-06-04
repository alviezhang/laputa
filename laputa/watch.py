#coding: utf-8

from .record import Recorder
from .notify import IFTTTNotifier
from .weibo  import WeiboUser


class Watcher:
    def __init__(self, weibo_uid, recorder=None, notifier=None):
        self._weibo_user = WeiboUser(weibo_uid)
        self._recorder = recorder
        self._notifier = notifier

    def set_recorder(self, recorder):
        self._recorder = recorder

    def set_notifier(self, notifier):
        self._notifier = notifier

    def watch(self):
        self._watch_event('posts')
        self._watch_event('likes')

    def _watch_event(self, watch_type):
        last_data = self._recorder.read()
        if watch_type in ('posts', 'likes'):
            action_name = {
                'posts': '发布',
                'likes': '赞',
            }
            value1 = action_name[watch_type]
            last_watch = last_data[watch_type]
            if last_watch:
                posts = self._weibo_user.get(watch_type, after=last_watch)
                for post in reversed(posts):
                    self._notifier.trigger(value1=value1, value2=post.text, value3=post.url)
                    last_watch = ([posts[0].id] + last_watch)[:10]
            else:
                posts = self._weibo_user.get(watch_type, size=1, after=last_watch)
                if posts:
                    last_watch = ([posts[0].id] + last_watch)[:10]
            self._recorder.write({watch_type: last_watch})

