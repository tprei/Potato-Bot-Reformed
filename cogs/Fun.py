import aiohttp
import asyncio
import io

from discord.ext import commands, tasks
from discord import File, Member

from datetime import datetime
from utils import config as cfg

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spamCount = 0

    async def randomImg(self, ctx, url, numImages=1):
        """Make a request to InspiroBot"""
        SUCESS = 200
        async with aiohttp.ClientSession() as session:
            for _ in range(numImages):
                async with session.get(url) as resp:
                    if resp.status != SUCESS:
                        await ctx.send('Could not generate image...')
                        return

                    async with session.get(await resp.text()) as img:
                        data = io.BytesIO(await img.read())
                        await ctx.send(file=File(data, 'img.png'))

    @commands.command()
    async def motivar(self, ctx, numImages=1):
        """Sends a motivational picture"""
        if numImages > 3:
            await ctx.send('OOOOOOOOOOUUOOUOU PAROU PAROU TA MUITO GRANDE ESSE NUMERO AI AMIGAO')
            return

        await self.randomImg(ctx, cfg.URLs['INSPIRO'], numImages)

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot server"""
        messages = await ctx.channel.history(limit=1).flatten()

        lastMsg = messages[0].created_at
        now = datetime.utcnow()

        await ctx.send(f'Pong! {(now-lastMsg).total_seconds() * 1000.0} ms')

    @tasks.loop(seconds=1)
    async def spamUser(self, ctx, member, cnt):
        await member.send(f'Ou {member} bora lol pls')
        self.spamCount += 1

    @commands.command()
    async def boralol(self, ctx, members: commands.Greedy[Member], *, k=cfg.MAX_BORALOL):
        """Vem pra flex manito"""

        if k > cfg.MAX_BORALOL:
            await ctx.send(f'PO MANO AI O SPAM TA DEMAIS NÉ')

        for member in members:
            for _ in range(k):
                await member.send(f'Ou {member} bora lol pls')

def setup(bot):
    bot.add_cog(Fun(bot))
