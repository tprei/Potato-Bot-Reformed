from discord.ext import commands
import os
from pantheon import pantheon


class Clash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.startup()

    def startup(self):
        api_key = os.getenv('RIOT_KEY')
        if api_key == None:
            return

        self.bot.panth = pantheon.Pantheon(
            'br1',
            api_key,
            errorHandling=True,
            debug=True
        )

    @commands.command()
    async def clash(self, ctx, username):
        data = await self.bot.panth.getSummonerByName(username.strip())
        if 'id' in data.keys():
            summonerId = data['id']
            player = await self.bot.panth.getClashPlayersBySummonerId(summonerId)
            if len(player) > 0 and 'teamId' in player[0].keys():
                team_id = player[0]['teamId']
                team = await self.bot.panth.getClashTeamById(team_id)

                message = ''
                for player in team['players']:
                    summoner = await self.bot.panth.getSummoner(player['summonerId'])
                    message += f'[{player["position"]}] {summoner["name"]}\n'

                await ctx.send(message)


def setup(bot):
    bot.add_cog(Clash(bot))
