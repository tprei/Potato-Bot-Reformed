import aiohttp
import asyncio
import io

from discord.ext import commands, tasks
from discord import File, Member

from datetime import datetime
from utils.config import GLOBAL as cfg

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def random_img(self, ctx, url, num_images=1):
        """Make a request to InspiroBot"""
        SUCESS = 200
        async with aiohttp.ClientSession() as session:
            for _ in range(num_images):
                async with session.get(url) as resp:
                    if resp.status != SUCESS:
                        await ctx.send('Não foi possível gerar a imagem.')
                        return

                    async with session.get(await resp.text()) as img:
                        data = io.BytesIO(await img.read())
                        await ctx.send(file=File(data, 'img.png'))

    @commands.command()
    async def motivar(self, ctx, num_images=1):
        """Manda uma imagem motivacional para aquecer vossos corações"""
        if num_images > 3:
            raise commands.BadArgument

        await self.random_img(ctx, cfg['URLs']['INSPIRO'], num_images)

    @motivar.error
    async def motivar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Comando deve ser no formato `>motivar k` onde k < 4')
        else:
            print(error)

    @commands.command()
    async def ping(self, ctx):
        """Pinga o bot pra saber se ele ta vivásso"""
        messages = await ctx.channel.history(limit=1).flatten()

        lastMsg = messages[0].created_at
        now = datetime.utcnow()

        await ctx.send(f'Pong! {(now-lastMsg).total_seconds() * 1000.0} ms')

    @commands.command()
    async def boralol(self, ctx, members: commands.Greedy[Member], *, message=cfg['MSG_BORALOL']):
        """Spamma o amiguinho pra chamar a atençao dele"""

        for member in members:
            for _ in range(cfg['MAX_BORALOL']):
                await member.send(message)

    @boralol.error
    async def boralol_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Um dos usuários informados não existe. =(')
        else:
            print(error)

def setup(bot):
    bot.add_cog(Fun(bot))
