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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        handler = self.bot.get_cog('GoldHandler')
        gold = self.bot.get_cog('Gold')
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        reaction = None
        for r in message.reactions:
            if str(r) == cfg['DEFAULT_GOLD_EMOJI']:
                reaction = r
                break

        if reaction is not None and await gold.check_gold(reaction, message.channel):
            await handler.handle(reaction)

def setup(bot):
    bot.add_cog(Events(bot))
