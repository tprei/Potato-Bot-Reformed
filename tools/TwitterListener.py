import asyncio
import threading
import tweepy
import urllib3

from utils.config import GLOBAL as cfg

class TwitterListener(tweepy.StreamListener):

    def __init__(self, cog):
        super().__init__()
        self.twitter_cog = cog
        self.cache = set()
        
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

    def on_status(self, status):
        if not self.from_creator(status) or status.id_str in self.cache:
            return

        url = f'https://www.twitter.com/{status.user.id}/status/{status.id_str}/'

        self.cache.add(status.id_str)
        bot = self.twitter_cog.bot
        channel = bot.get_channel(cfg['DEFAULT_TWITTER_CHANNEL'])
        
        bot.loop.create_task(channel.send(url))

    def on_error(self, status):
        if status == 420:
            print('Twitter error | Reconnecting...')
            return True

    def on_exception(self, exception):
        bot = self.twitter_cog.bot
        if isinstance(exception, urllib3.exceptions.ReadTimeoutError):
            print(f'Twitter stream timed out | Recreating stream...')
        elif isinstance(exception, urllib3.exceptions.ProtocolError):
            print(f'Twitter stream read error | Recreating stream...')
        else:
            print(exception)

        bot.loop.create_task(self.twitter_cog.reset())
