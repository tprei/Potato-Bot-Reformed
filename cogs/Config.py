from discord.ext import commands

from utils.config import GLOBAL as cfg, add_global, remove_global

from json import dumps

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @commands.is_owner()
    async def config(self, ctx):
        pretty_json = dumps(cfg, sort_keys=True, indent=4)
        await ctx.send(f'```json\n{pretty_json}\n```')

    @config.command(aliases=['edit', 'add'])
    @commands.is_owner()
    async def set(self, ctx, key: str, value: str, is_int=0):
        if is_int:
            value = int(value)
        add_global(key, value)

    @config.command(aliases=['erase', 'remove'])
    @commands.is_owner()
    async def rmv(self, ctx, key: str):
        remove_global(key)

def setup(bot):
    bot.add_cog(Config(bot))
