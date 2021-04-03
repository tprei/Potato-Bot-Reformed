import aiohttp
import asyncio
import io

from discord.ext import commands, tasks
from discord import File, Member

from datetime import datetime

from utils.config import GLOBAL as cfg, EMOJI
from utils.helper import remove_special_chars as fix_string
from utils.stopwords import stopwords

import random

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

    @commands.command()
    async def zap(self, ctx):
        """Zapifica sua mensagem."""
        rows = ctx.message.content.split('\n')

        for i in range(len(rows)):
            rows[i] = rows[i].split()

        rows[0] = rows[0][1:]
        
        new_sentence = ""

        """https://github.com/vmarchesin/vemdezapbe.be/blob/master/api/db/tokens.js"""
        for r in rows:
            for word in r:
                new_sentence += word + ' '
                fixed = await fix_string(word)

                if fixed in stopwords or len(fixed) < 2:
                    continue

                rng = random.randint(1, 10)

                if fixed in EMOJI['full_match'] or fixed in EMOJI['full_match_extra']:
                    extra_rng = random.randint(1, 10)

                    if fixed in EMOJI['full_match']:
                        index_rng = random.randint(1, 10)
                        # 10% of odds of not getting first emoji
                        if index_rng < 2:
                            random_emoji = random.choice(EMOJI['full_match'][fixed])
                        else:
                            random_emoji = EMOJI['full_match'][fixed][0]

                    # 60% odds
                    elif extra_rng >= 4:
                        index_rng = random.randint(1, 10)
                        if index_rng < 3:
                            random_emoji = random.choice(EMOJI['full_match_extra'][fixed])
                        else:
                            random_emoji = EMOJI['full_match_extra'][fixed][0]
                    else:
                        continue

                    random_qt = random.randint(1, 3)
                    new_sentence += random_qt * random_emoji + ' '
                    continue

                # 80% of chance of adding an emoji
                if rng <= 2:
                    continue

                for prefix in EMOJI['partial_match']:
                    if fixed.startswith(prefix):
                        random_emoji = random.choice(EMOJI['partial_match'][prefix])
                        random_qt = random.randint(1, 3)
                        new_sentence += random_qt * random_emoji + ' '
                        break
            new_sentence += '\n'

        await ctx.send(new_sentence)

    @commands.command()
    async def zap_unicode(self, ctx):
        """Zapifica sua mensagem utilizando emojis em unicode"""
        rows = ctx.message.content.split('\n')

        for i in range(len(rows)):
            rows[i] = rows[i].split()

        rows[0] = rows[0][1:]
        
        new_sentence = ""

        """https://github.com/vmarchesin/vemdezapbe.be/blob/master/api/db/tokens.js"""
        for r in rows:
            for word in r:
                new_sentence += word + ' '
                fixed = await fix_string(word)

                if fixed in stopwords or len(fixed) < 2:
                    continue

                rng = random.randint(1, 10)

                if fixed in EMOJI['full_match'] or fixed in EMOJI['full_match_extra']:
                    extra_rng = random.randint(1, 10)

                    if fixed in EMOJI['full_match']:
                        index_rng = random.randint(1, 10)
                        # 10% of odds of not getting first emoji
                        if index_rng < 2:
                            random_emoji = random.choice(EMOJI['full_match'][fixed])
                        else:
                            random_emoji = EMOJI['full_match'][fixed][0]

                    # 60% odds
                    elif extra_rng >= 4:
                        index_rng = random.randint(1, 10)
                        if index_rng < 3:
                            random_emoji = random.choice(EMOJI['full_match_extra'][fixed])
                        else:
                            random_emoji = EMOJI['full_match_extra'][fixed][0]
                    else:
                        continue

                    random_qt = random.randint(1, 3)
                    new_sentence += random_qt * ('\\' + random_emoji + ' ')
                    continue

                # 80% of chance of adding an emoji
                if rng <= 2:
                    continue

                for prefix in EMOJI['partial_match']:
                    if fixed.startswith(prefix):
                        random_emoji = random.choice(EMOJI['partial_match'][prefix])
                        random_qt = random.randint(1, 3)
                        new_sentence += random_qt * ('\\' + random_emoji + ' ')
                        break
            new_sentence += '\n'

        await ctx.send(new_sentence)

def setup(bot):
    bot.add_cog(Fun(bot))
