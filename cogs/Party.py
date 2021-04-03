import asyncio
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from discord import NotFound

from tools.PartyEmbed import PartyEmbed

from utils.config import GLOBAL as cfg


class Party(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.party_cleanup.start()
        self.party_join_emoji = cfg['COMMANDS_SUCCESS']
        self.party_close_emoji = cfg['COMMANDS_FAILURE']

    @staticmethod
    def create_party(msg, game, party_size, ttl):
        return {
            "joined": {msg.author: None},
            "party_size": party_size,
            "game": game,
            "channel": msg.channel,
            "owner": msg.author,
            "created_at": datetime.now(),
            "ttl": ttl
        }

    async def close_party(self, party, msg):
        # send party summary
        closed_party = PartyEmbed(party, description='**A party fechou!**')
        joined = party['joined']

        del party  # remove party object from dict
        await msg.edit(embed=closed_party)  # remove party message
        await msg.reply(content=" ".join([j.mention for j in joined.keys()]))

    @tasks.loop(minutes=1)
    async def party_cleanup(self):
        must_remove = []
        parties = self.bot.active_parties.items()
        for k, v in parties:
            creation = v['created_at']
            ttl = v['ttl']
            if (datetime.now() - creation).total_seconds() / 60.0 > ttl:
                must_remove.append(k)
                try:
                    msg = await v['channel'].fetch_message(k)
                    if msg is not None:
                        await msg.delete()
                except NotFound:
                    pass

        for i in must_remove:
            del self.bot.active_parties[i]

    @party_cleanup.before_loop
    async def before_checker(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        msg_id = payload.message_id
        emoji = payload.emoji
        user = await self.bot.fetch_user(payload.user_id)

        if str(emoji) == str(self.party_join_emoji):
            # if message is not a party proposal
            if msg_id not in self.bot.active_parties:
                return

            party = self.bot.active_parties[msg_id]
            channel = self.bot.get_channel(cfg['DEFAULT_PARTY_CHANNEL'])
            msg = await channel.fetch_message(msg_id)

            if user in party['joined'] and user != party['owner']:
                del party['joined'][user]
                embed = PartyEmbed(party)
                await msg.edit(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        msg_id = msg.id
        emoji = reaction.emoji

        if user == self.bot.user:  # check if its not bot
            return
        if msg_id not in self.bot.active_parties:  # if message is not a party proposal
            return

        party = self.bot.active_parties[msg_id]
        joined = party['joined']

        if emoji == self.party_join_emoji:
            if user == party['owner']:  # if user is the party owner
                return

            joined[user] = None

            # check if party is complete
            if len(joined) == party['party_size']:
                await self.close_party(party, msg)
            else:
                embed = PartyEmbed(party)
                await msg.edit(embed=embed)
        elif emoji == self.party_close_emoji:
            if user != party['owner']:  # if user is NOT the party owner
                return

            await self.close_party(party, msg)

    @commands.command()
    async def party(self, ctx, game: str, party_size=5, ttl=300):
        msg = ctx.message
        party_obj = self.create_party(msg, game, party_size, ttl)
        embed = PartyEmbed(party_obj)

        channel_id = cfg['DEFAULT_PARTY_CHANNEL']
        channel = self.bot.get_channel(channel_id)
        embed_msg = await channel.send(embed=embed)

        await embed_msg.add_reaction(cfg['COMMANDS_SUCCESS'])
        await embed_msg.add_reaction(cfg['COMMANDS_FAILURE'])

        self.bot.active_parties[embed_msg.id] = party_obj


def setup(bot):
    bot.add_cog(Party(bot))
