from discord.ext import commands

from utils.config import GLOBAL as cfg, add_global

# Known bug: Doesn't support multiple embeds

class GoldChannelNotFound(Exception):
    """Raised when Gold channel is unspecified in utils/config.json"""
    pass

class Gold(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_random_gold(self):
        pass

    async def get_gold_channel(self, ctx):
        return await self.bot.fetch_channel(cfg['DEFAULT_GOLD_CHANNEL'])

    @commands.group()
    async def gold(self, ctx):
        """Gets random golded message"""
        pass
        gold_channel = await get_gold_channel()
        

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

def setup(bot):
    bot.add_cog(Gold(bot))
