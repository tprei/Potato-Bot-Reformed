from discord import Embed

from utils.config import GLOBAL as cfg
from tools.GoldEmbed import GoldEmbed

def get_message_info(reaction):
    return cfg['DEFAULT_GOLD_EMOJI'], reaction.count, reaction.message.channel

def make_message(emoji, count, channel, username):
    msg = f'{emoji} **{count}** em {channel.mention}' 
    msg += '' if username == None else ' por ' + username
    return msg


async def send_gold_message(reaction, to_channel, _embed, gold_files):
    emoji, count, from_channel = get_message_info(reaction)

    if not isinstance(_embed, GoldEmbed):
        user = reaction.message.author.mention
    else:
        user = None

    if _embed != Embed.Empty:
        message = await to_channel.send(make_message(emoji, count, from_channel, user), embed=_embed, files=gold_files)
    else:
        message = await to_channel.send(make_message(emoji, count, from_channel, user), files=gold_files)

    return message

async def edit_gold_message(message, reaction):

    emoji, count, from_channel = get_message_info(reaction)

    _embed = message.Embeds[0]

    if not isinstance(_embed, GoldEmbed):
        user = reaction.message.author.mention
    else:
        user = None

    new_content = make_message(emoji, count, from_channel, user) 

    await message.edit(content=new_content)
