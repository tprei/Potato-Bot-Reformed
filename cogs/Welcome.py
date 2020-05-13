from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.wait_until_ready()
        potato_clan = member.guild
        guild_roles = potato_clan.roles

        for role in guild_roles:
            if role.name == 'batatinha':
                batatinha = role

        await member.add_roles(batatinha, reason='Member joined.')

def setup(bot):
    bot.add_cog(Welcome(bot))
