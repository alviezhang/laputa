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
        if watch_type == 'posts':
            last_post = last_data['post']
            if last_post == 0:
                posts = self._weibo_user.get('posts', size=1, after=last_post)
                if posts:
                    last_post = posts[0].id
            else:
                posts = self._weibo_user.get('posts', after=last_post)
                for post in reversed(posts):
                    self._notifier.trigger(value1='发表', value2=post.text, value3=post.url)
                    last_post = post.id
            self._recorder.write({'post': last_post})
        elif watch_type == 'likes':
            last_like = last_data['like']
            if last_like == 0:
                posts = self._weibo_user.get('likes', size=1, after=last_like)
                if posts:
                    last_like = posts[0].id
            else:
                posts = self._weibo_user.get('likes', after=last_like)
                for post in reversed(posts):
                    self._notifier.trigger(value1='赞', value2=post.text, value3=post.url)
                    last_like = post.id
            self._recorder.write({'like': last_like})
