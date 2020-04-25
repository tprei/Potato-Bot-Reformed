from utils.config import GLOBAL as cfg
from discord.ext import commands

def make_message(emoji, count, channel):
    return f'{emoji} **{count}** in {channel.mention}'

def get_message_info(reaction):
    return cfg['DEFAULT_GOLD_EMOJI'], reaction.count, reaction.message.channel

async def send_gold_message(reaction, to_channel, gold_embed):
    emoji, count, from_channel = get_message_info(reaction)

    message = await to_channel.send(make_message(emoji, count, from_channel), embed=gold_embed)
    
    return message

async def edit_gold_message(message, reaction):

    emoji, count, from_channel = get_message_info(reaction)

    new_content = make_message(emoji, count, from_channel) 

    await message.edit(content=new_content)

def is_owner():
    async def condition(ctx):
        return ctx.author.id == cfg['OWNER']
    return commands.check(condition)
