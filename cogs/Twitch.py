from datetime import datetime
from discord import Embed, Colour, File
from discord.ext import commands, tasks
from utils.config import GLOBAL as cfg

import aiohttp
import json
import os

class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_stream.start()
        self.last_time = datetime.now()
        self.stopped = True

    async def fetch_json(self, session, url, headers):
        async with session.get(url, headers=headers) as response:
            return await response.json()

    async def fetch_image(self, session, url):
        async with session.get(url) as response:
            return await response.read()

    @tasks.loop(minutes=5)
    async def check_stream(self):
        token = os.environ.get('TWITCH_TOKEN')

        client_id = cfg['TWITCH_CLIENT_ID']
        user_id = cfg['TWITCH_USER_ID']

        if token is None:
            raise RuntimeError('TWITCH_TOKEN is not set in environment variables.')

        
        auth = 'Bearer ' + token
        headers = {
                'Authorization': auth,
                'Client-ID': client_id,
        }

        url = 'https://api.twitch.tv/helix/streams?user_id=' + str(user_id)

        async with aiohttp.ClientSession() as session:
            twitch_response = await self.fetch_json(session, url, headers)
            channel_id = cfg['DEFAULT_ANNOUNCE_CHANNEL']
            channel = self.bot.get_channel(channel_id)

            last_stream = (datetime.now() - self.last_time).total_seconds() / 3600.0

            if len(twitch_response['data']) > 0 and (last_stream > 3.0 or self.stopped):
                title = twitch_response['data'][0]['title']
                thumbnail = twitch_response['data'][0]['thumbnail_url']
                username = twitch_response['data'][0]['user_name']
                description = username + ' acaba de entrar em live!' + '<:batataThinking:731871457470316574>' + '\n https://www.twitch.tv/' + username 

                thumbnail = thumbnail.replace('{width}', '1280')
                thumbnail = thumbnail.replace('{height}', '720')

                img = await self.fetch_image(session, thumbnail)

                with open('twitch_thumbnail.png', 'wb') as f:
                    f.write(img)

                file = File("twitch_thumbnail.png", filename="image.png")

                colour = Colour.dark_purple()

                embed = Embed (
                        title=title,
                        type='rich',
                        colour=colour,
                        description=description
                )

                embed = embed.set_image(url="attachment://image.png")
                await channel.send(file=file, embed=embed)

                self.last_time = datetime.now()
                self.stopped = False
            elif len(twitch_response['data']) == 0:
                self.stopped = True

    @check_stream.before_loop
    async def before_checker(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Twitch(bot))
