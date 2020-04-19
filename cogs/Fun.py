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
                        await ctx.send('Não foi possível gerar a imagem.')
                        return

                    async with session.get(await resp.text()) as img:
                        data = io.BytesIO(await img.read())
                        await ctx.send(file=File(data, 'img.png'))

    @commands.command()
    async def motivar(self, ctx, numImages=1):
        """Manda uma imagem motivacional para aquecer vossos corações"""
        if numImages > 3:
            await ctx.send('Po esse numero aí ta muito grande.')
            return

        await self.randomImg(ctx, cfg.URLs['INSPIRO'], numImages)

    @motivar.error
    async def motivarError(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Comando deve ser no formato `>motivar k` onde k é um número inteiro.')

    @commands.command()
    async def ping(self, ctx):
        """Pinga o bot pra saber se ele ta vivásso"""
        messages = await ctx.channel.history(limit=1).flatten()

        lastMsg = messages[0].created_at
        now = datetime.utcnow()

        await ctx.send(f'Pong! {(now-lastMsg).total_seconds() * 1000.0} ms')

    @commands.command()
    async def boralol(self, ctx, members: commands.Greedy[Member], *, k=cfg.MAX_BORALOL):
        """Vem pra flex manito"""

        if k > cfg.MAX_BORALOL:
            await ctx.send(f'Ai o spam ta muito grande né manito, quer spammar assim vai pro caralho')
            return

        await ctx.send(f'To chamando os fera pro lolzin')
        for member in members:
            for _ in range(k):
                await member.send(f'Ou {member} bora lol pls')

    @boralol.error
    async def boralolError(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Um dos usuários informados não existe. =(')

def setup(bot):
    bot.add_cog(Fun(bot))
