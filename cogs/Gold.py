from discord.ext import commands
from discord import TextChannel, Forbidden, Embed

from utils.config import GLOBAL as cfg, add_global

import re

class Gold(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_random_gold(self):
        pass

    async def get_gold_channel(self):
        return await self.bot.fetch_channel(cfg['DEFAULT_GOLD_CHANNEL'])

    @commands.group(case_insensitive=True)
    async def gold(self, ctx):
        """Gets random golded message"""
        pass
        gold_channel = await self.get_gold_channel()
    
    @gold.command()
    @commands.is_owner()
    async def build(self, ctx, ch: TextChannel):
        await ctx.send(f"This may take a while, building golds from channel {ch}")
        handler = self.bot.get_cog('GoldHandler')

        try:
            async for message in ch.history(limit=5000):
                reactions = message.reactions
                for reaction in reactions:
                    if await self.check_gold(reaction, ch):
                        embed_id = await self.bot.gold_db.lookup(message.id)

                        if embed_id is None:
                            await handler.handle(reaction)
        except Forbidden:
            await ctx.send("I don't have permission to access that channel's history.")
    
    @gold.command()
    @commands.is_owner()
    async def restore(self, ctx):
        await ctx.send(f"This may take a while, restoring golds from gold channel")
        gold_channel = await self.get_gold_channel()
        bindings = dict()
        async for message in gold_channel.history(limit=None):
            if len(message.embeds) > 0 and type(message.embeds[0].description) == str:
                obj = re.search('https.+?(?=\))', message.embeds[0].description)

                if obj:
                    original_id = obj.group(0).split('/')[-1]
                    embed_id = await self.bot.gold_db.lookup(original_id)

                    if embed_id is None:
                        bindings[original_id] = message.id
        
        await self.bot.gold_db.insert_many(list(zip(list(bindings), list(bindings.values()))))


    @gold.command(aliases=['set'])
    @commands.is_owner()
    async def emoji(self, ctx, emoji):
        """Setup your golded message emoji!"""
        add_global('DEFAULT_GOLD_EMOJI', emoji)

    @gold.command(aliases=['stat', 'info'])
    async def stats(self, ctx):
        """Gets stats for golded messages"""
        pass

    @gold.command()
    async def limit(self, ctx, L:int):
        """Sets the minimum threshold for golded messages"""
        add_global('DEFAULT_GOLD_LIMIT', L)

    @gold.error
    @emoji.error
    @limit.error
    async def gold_error(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send('Wrong argument. See `>help gold`')
        else:
            print(error)

    async def check_gold(self, reaction, channel):
        count = reaction.count
        channel_id = channel.id

        # must be gold emoji
        if str(reaction) != cfg['DEFAULT_GOLD_EMOJI']:
            return False

        # must surpass minimum
        if count < cfg['DEFAULT_GOLD_LIMIT']:
            return False

        # can't be message from gold channel
        if channel_id == cfg['DEFAULT_GOLD_CHANNEL']:
            return False

        return True


def setup(bot):
    bot.add_cog(Gold(bot))
