from discord.ext import commands
from discord import Embed

from tools.GoldEmbed import GoldEmbed
from tools.GoldMessage import send_gold_message, edit_gold_message

class GoldHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gold_channel = None

    async def fetch_gold_channel(self):
        gold_cog = self.bot.get_cog('Gold')
        return await gold_cog.get_gold_channel()

    async def create_gold(self, reaction):
        # for some reason you can't send multiple embeds in the TextChannel send coroutine
        message = reaction.message
        attachments = message.attachments
        embed = GoldEmbed(message)

        if embed.simple:
            files = []
            if len(message.embeds) > 0:
                embed = message.embeds[0]
        else:
            files = [await attach.to_file() for attach in attachments]
            embed = Embed.Empty

        sent_message = await send_gold_message(reaction, self.gold_channel, embed, files)

        self.bot.gold_ids[message.id] = sent_message.id

    async def update_gold(self, reaction):
        message = reaction.message
        embed_id = self.bot.gold_ids[message.id]
        emb_message = await self.gold_channel.fetch_message(embed_id)
        await edit_gold_message(emb_message, reaction)

    async def handle(self, reaction):
        message = reaction.message
        embed = GoldEmbed(message)
       
        if self.gold_channel == None:
            self.gold_channel = await self.fetch_gold_channel()

        # if gold message already exists
        if message.id in self.bot.gold_ids:
            await self.update_gold(reaction)
        else:
            await self.create_gold(reaction)

def setup(bot):
    bot.add_cog(GoldHandler(bot))
