import aiohttp
import asyncio
import io

from discord.ext import commands
from discord import File

INSPIRO_URL = 'https://inspirobot.me/api?generate=true'

async def asyncRange(start, stop=None, step=1):
    if stop:
        range_ = range(start, stop, step)
    else:
        range_ = range(start)

    for i in range_:
        yield i
        await asyncio.sleep(0)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def randomImg(self, ctx, url, numImages=1):
        SUCESS = 200
        async with aiohttp.ClientSession() as session:
            async for _ in asyncRange(numImages):
                async with session.get(url) as resp:
                    if resp.status != SUCESS:
                        await ctx.send('Could not generate image...')
                        return

                    async with session.get(await resp.text()) as img:
                        data = io.BytesIO(await img.read())
                        await ctx.send(file=File(data, 'img.png'))

    @commands.command(aliases=['motivar'])
    async def motivate(self, ctx, numImages=1):
        if numImages > 3:
            await ctx.send('OOOOOOOOOOUUOOUOU PAROU PAROU TA MUITO GRANDE ESSE NUMERO AI AMIGAO')
            return

        await self.randomImg(ctx, INSPIRO_URL, numImages)

def setup(bot):
    bot.add_cog(Fun(bot))
