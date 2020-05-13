import asyncio
import threading
import tweepy

from utils.config import GLOBAL as cfg

def fetch_twitter_channel():
    return cfg['DEFAULT_TWITTER_CHANNEL']

class TwitterListener(tweepy.StreamListener):

    def __init__(self, channel, bot):
        super().__init__()
        self.twitter_channel = channel
        self.bot = bot

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
        if not self.from_creator(status):
            return

        url = f'https://www.twitter.com/{status.user.id}/status/{status.id_str}/'

        self.bot.loop.create_task(self.twitter_channel.send(url))

    def on_error(self, status):
        if status == 420:
            print('Disconnecting from Twitter')
            return False

    async def stop(self):
        self.running = False
