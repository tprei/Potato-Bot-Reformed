from discord.ext import commands
from utils.config import GLOBAL as cfg

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        print("\n")

        print(" ▄▄▄·     ▄▄▄▄▄ ▄▄▄·▄▄▄▄▄          ▄▄▄▄·      ▄▄▄▄▄")
        print("▐█ ▄█▪    •██  ▐█ ▀█•██  ▪         ▐█ ▀█▪▪    •██")
        print(" ██▀· ▄█▀▄ ▐█.▪▄█▀▀█ ▐█.▪ ▄█▀▄     ▐█▀▀█▄ ▄█▀▄ ▐█.▪")
        print("▐█▪·•▐█▌.▐▌▐█▌·▐█ ▪▐▌▐█▌·▐█▌.▐▌    ██▄▪▐█▐█▌.▐▌▐█▌·")
        print(".▀    ▀█▄▀▪▀▀▀  ▀  ▀ ▀▀▀  ▀█▄▀▪    ·▀▀▀▀  ▀█▄▀▪▀▀▀")

        print("\n")

        print(f'Logged in as {self.bot.user}')

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


    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await ctx.message.add_reaction(cfg['COMMANDS_SUCCESS'])

    def check_gold(self, reaction, channel):
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

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        handler = self.bot.get_cog('GoldHandler')
        message = reaction.message

        if self.check_gold(reaction, message.channel):
            await handler.handle(reaction)

def setup(bot):
    bot.add_cog(Events(bot))
