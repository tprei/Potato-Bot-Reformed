from discord.ext import commands
from tools.TwitterListener import TwitterListener
from utils.config import GLOBAL as cfg, add_global, remove_entry

import asyncio
import os
import tweepy

class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        try:
            self.api = self.authenticate()
            self.stream = None
        except:
            print('Could not authenticate to Twitter API')

        self.bot.loop.create_task(self.start())

    def authenticate(self):
        try:
            consumer_key = os.environ.get('CONSUMER_KEY')
            consumer_secret = os.environ.get('CONSUMER_SECRET')
            access_token = os.environ.get('ACCESS_TOKEN')
            access_secret = os.environ.get('ACCESS_TOKEN_SECRET')
        except:
            print('Must define Twitter auth keys as environment variables in .bashrc')
            return

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        return tweepy.API(auth)

    async def add_user(self, user_id):
        add_global('FOLLOW', user_id, append=True)

    async def rmv_user(self, user_id):
        remove_entry('FOLLOW', user_id)

    @commands.group(case_insensitive=True)
    async def twitter(self, ctx):
        pass

    @twitter.command(aliases=['show'])
    async def list(self, ctx):
        follow_list = cfg['FOLLOW']

        if len(follow_list) == 0:
            await ctx.send('O bot não está seguindo ninguém =(.')
            return

        msg = "Lista de seguidores do bot: \n```"
        for user_id in follow_list:
            user = self.api.get_user(id=user_id)
            msg += user.screen_name + '\n'

        msg += "```"
        await ctx.send(msg)

    @twitter.command(aliases=['follow'])
    async def add(self, ctx, user):
        try:
            user = self.api.get_user(screen_name=user)
        except Exception as e:
            await ctx.send('Usuário inválido.')
            print(e)
            return

        print('User added to follow list | Resetting Twitter timeline')
        await self.add_user(user.id)
        await self.reset()

    @twitter.command(aliases=['unfollow'])
    async def rmv(self, ctx, user):
        try:
            user = self.api.get_user(screen_name=user)
        except Exception as e:
            await ctx.send('Usuário inválido.')
            print(e)
            return

        print('User removed from follow list | Resetting Twitter timeline')
        await self.rmv_user(user.id)
        await self.reset()

    async def reset(self):
        '''Resets the tweepy stream object (in case any changes were made to filters'''
        try:
            follow_list = list(map(str, cfg['FOLLOW']))
            self.stream = tweepy.Stream(auth=self.api.auth, listener=self.listener)
            
            self.stream.filter(follow=follow_list, is_async=True)
        except Exception as e:
            print('Stream Error: Stream never initialized')
            print(e)

    @twitter.command(aliases=['reset'])
    @commands.is_owner()
    async def reset_command(self, ctx):
        await self.reset()


    async def start(self):
        await self.bot.wait_until_ready()

        channel_id = cfg['DEFAULT_TWITTER_CHANNEL']
        self.twitter_channel = self.bot.get_channel(channel_id)

        self.listener = TwitterListener(self)
 
        print('Starting bot | Resetting Twitter timeline')
        await self.reset()

    @twitter.command(alises=['halt', 'kill'])
    @commands.is_owner() 
    async def stop(self):
        await self.listener.stop()


def setup(bot):
    bot.add_cog(Twitter(bot))
