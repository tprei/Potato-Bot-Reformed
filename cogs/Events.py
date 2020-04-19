from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print('Starting bot =)\n===========================\n')
        print(f'Logged in as --> {self.bot.user}')

    async def on_message(self, message):
        if message.author == bot.user:
            return

        print('> {message.author}: {message.content}')

def setup(bot):
    bot.add_cog(Events(bot))

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

def setup(bot):
    bot.add_cog(Events(bot))
