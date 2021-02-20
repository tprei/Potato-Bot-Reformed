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

    @staticmethod
    def create_party(msg, game, party_size, ttl):
        return {
            "joined": [msg.author],
            "party_size": party_size,
            "game": game,
            "channel": msg.channel,
            "owner": msg.author,
            "created_at": datetime.now(),
            "ttl": ttl
        }

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
    async def on_reaction_remove(self, reaction, user):
        msg = reaction.message
        msg_id = msg.id
        emoji = reaction.emoji

        if emoji == self.party_join_emoji:
            # if message is not a party proposal
            if msg_id not in self.bot.active_parties:
                return

            party = self.bot.active_parties[msg_id]
            if user in party['joined'] and user != party['owner']:
                party['joined'].remove(user)
                embed = PartyEmbed(party)
                await msg.edit(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message
        msg_id = msg.id
        emoji = reaction.emoji

        if user == self.bot.user:  # check if its not bot
            return

        if emoji == self.party_join_emoji:
            # if message is not a party proposal
            if msg_id not in self.bot.active_parties:
                return

            party = self.bot.active_parties[msg_id]
            joined = party['joined']

            if user == party['owner']:
                return
            else:
                joined.append(user)

            # check if party is complete
            if len(joined) == party['party_size']:
                # send party summary
                closed_party = PartyEmbed(party, description='**A party fechou!**')

                del party  # remove party object from dict
                await msg.edit(embed=closed_party)  # remove party message
                await msg.reply(content=" ".join([j.mention for j in joined]))
            else:
                embed = PartyEmbed(party)
                await msg.edit(embed=embed)

    @commands.command()
    async def party(self, ctx, game: str, party_size=5, ttl=60):
        msg = ctx.message
        party_obj = self.create_party(msg, game, party_size, ttl)
        embed = PartyEmbed(party_obj)

        embed_msg = await ctx.send(embed=embed)
        await embed_msg.add_reaction(cfg['COMMANDS_SUCCESS'])
        self.bot.active_parties[embed_msg.id] = party_obj


def setup(bot):
    bot.add_cog(Party(bot))
