import argparse
import asyncio
import json
import os
import time
from pprint import pprint
from urllib.parse import quote

import gspread_asyncio
from discord.ext import commands
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pantheon import pantheon


def opgg(name):
    return 'https://br.op.gg/summoner/userName={}'.format(quote(name))


def cell_values(names, clear=False):
    if clear:
        return ["" for i in range(len(names))]
    else:
        formulas = [None if names[i] is None else "=HYPERLINK(\"{}\", \"{}\")".format(
            opgg(names[i]), names[i]) for i in range(len(names))]
        return formulas


class Clash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.startup()

    def _get_creds(self):
        # To obtain a service account JSON file, follow these steps:
        # https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account
        default_scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(self.sheets_path)
        scoped = creds.with_scopes(default_scopes)
        return scoped

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

        sheets_key = os.getenv('SHEETS_KEY')
        if sheets_key == None:
            return
        self.sheets_path = sheets_key

        self.agcm = gspread_asyncio.AsyncioGspreadClientManager(
            self._get_creds, loop=self.bot.loop)

    async def fill_cells_batch(self, formulas, game_id: int):
        agc = await self.agcm.authorize()

        sheet = await agc.open_by_key('1swBglL31meAvF4WSSrEbnBoWzlo8QnBjbLKcKMl3XX4')
        worksheet = await sheet.worksheet(f'Game {game_id}')
        cells = await worksheet.range('C15:I15')

        updates = []
        for i, cell in enumerate(cells):
            if formulas[i] is not None:
                updates.append(
                    {'range': cell.address, 'values': [[formulas[i]]]})
        await worksheet.batch_update(updates, value_input_option='USER_ENTERED')

    @commands.command()
    async def clash(self, ctx, username: str, *, game_id: int):
        data = await self.bot.panth.getSummonerByName(username.strip())
        if 'id' in data.keys():
            summonerId = data['id']
            player = await self.bot.panth.getClashPlayersBySummonerId(summonerId)
            if len(player) > 0 and 'teamId' in player[0].keys():
                team_id = player[0]['teamId']
                team = await self.bot.panth.getClashTeamById(team_id)

                message = ''
                roles = {}
                for player in team['players']:
                    summoner = await self.bot.panth.getSummoner(player['summonerId'])
                    message += f'[{player["position"]}] {summoner["name"]}\n'

                    roles[player['position']] = summoner['name']

                names = [
                    roles.get('TOP'),
                    roles.get('JUNGLE'),
                    roles.get('MIDDLE'),
                    roles.get('BOTTOM'),
                    roles.get('UTILITY'),
                    roles.get('FILL'),
                    roles.get('UNSELECTED')
                ]

                formulas = cell_values(names)
                await self.fill_cells_batch(formulas, game_id=game_id)
                await ctx.send(message)


def setup(bot):
    bot.add_cog(Clash(bot))
