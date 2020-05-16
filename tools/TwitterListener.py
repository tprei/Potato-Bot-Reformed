import asyncio
import threading
import tweepy
import urllib3

from utils.config import GLOBAL as cfg

from queue import Queue
from threading import Thread

NUM_THREADS = 5

class TwitterListener(tweepy.StreamListener):

    def __init__(self, cog, q = Queue()):
        super().__init__()
        self.twitter_cog = cog
        self.q = q

        for i in range(NUM_THREADS):
            t = Thread(target=self.fetch_queue)
            t.daemon = True
            t.start()
        
    def from_creator(self, status):
        """https://github.com/tweepy/tweepy/issues/981#issuecomment-393817367"""

        if hasattr(status, 'retweeted_status'):
            return False

        possible_mentions = [
                status.in_reply_to_status_id,
                status.in_reply_to_screen_name,
                status.in_reply_to_user_id
        ]

        return possible_mentions.count(None) == len(possible_mentions)
    
    def fetch_queue(self):
        while True:
            status = self.q.get()

            if not self.from_creator(status) or status.id_str in self.twitter_cog.bot.cache:
                self.q.task_done()
                continue

            url = f'https://www.twitter.com/{status.user.id}/status/{status.id_str}/'

            bot = self.twitter_cog.bot
            bot.cache.add(status.id_str)
            channel = bot.get_channel(cfg['DEFAULT_TWITTER_CHANNEL'])
            
            bot.loop.create_task(channel.send(url))
            self.q.task_done()

    def on_status(self, status):
        self.q.put(status)

    def on_error(self, status):
        if status == 420:
            print('Twitter error | Disconnecting...')

            bot = self.twitter_cog.bot
            bot.loop.create_task(self.twitter_cog.reset())
            return False

    def on_exception(self, exception):
        bot = self.twitter_cog.bot
        if isinstance(exception, urllib3.exceptions.ReadTimeoutError):
            print(f'Twitter stream timed out | Recreating stream...')
        elif isinstance(exception, urllib3.exceptions.ProtocolError):
            print(f'Twitter stream read error | Recreating stream...')
        else:
            print(exception)

        bot.loop.create_task(self.twitter_cog.reset())

