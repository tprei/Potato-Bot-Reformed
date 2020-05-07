from discord.ext import commands
from utils.config import GLOBAL as cfg
from utils.GoldEmbed import GoldEmbed
from utils.helper import send_gold_message, edit_gold_message

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
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if str(reaction) == cfg['DEFAULT_GOLD_EMOJI'] and reaction.count >= cfg['DEFAULT_GOLD_LIMIT'] and message.channel.id != cfg['DEFAULT_GOLD_CHANNEL']:
            # Create the embed
            embed = GoldEmbed(reaction.message)

            gold_cog = self.bot.get_cog('Gold')
            
            try:
                gold_channel = await gold_cog.get_gold_channel()
            except Exception as e:
                await message.channel.send('Gold channel must be configured')
                print(e)
                return

            if message.id in self.bot.gold_ids:
                embed_id = self.bot.gold_ids[message.id]
                emb_message = await gold_channel.fetch_message(embed_id)

                await edit_gold_message(emb_message, reaction)
            else:
                # for some reason you can't send multiple embeds in the TextChannel send coroutine
                if len(message.embeds) == 1:
                    embed = message.embeds[0]
            
                attachments = message.attachments
                files = [await attach.to_file() for attach in attachments]
                sent_message = await send_gold_message(reaction, gold_channel, embed, files)

                self.bot.gold_ids[message.id] = sent_message.id
                

def setup(bot):
    bot.add_cog(Events(bot))
