from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Starting bot =)\n===========================\n')
        print(f'Logged in as --> {self.bot.user}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        print(f'> {message.author}: {message.content}')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        print(f'x [DELETED] {message.author}: {message.content}')

def setup(bot):
    bot.add_cog(Events(bot))
