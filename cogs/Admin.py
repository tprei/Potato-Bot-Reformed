from discord.ext import commands
from discord.errors import NotFound
from utils.config import GLOBAL as cfg

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, num_messages=cfg['DEFAULT_CLEAR']):
        """Limpa as últimas mensagens. Por padrão 10, mas pode ser especificado."""
        messages = await ctx.channel.history(limit=num_messages).flatten()
        for i in range(1, len(messages)):
            await messages[i].delete();

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, NotFound): 
            print('All messages in the channel were deleted already.')
        else:
            print(error)
            await ctx.send(f'Eu não possuo permissão para deletar mensagens.')

    @commands.command()
    async def clearcm(self, ctx, num_messages=cfg['DEFAULT_CLEAR'], prefix=cfg['COMMANDS_PREFIX']):
        """Limpa os últimos comandos. Por padrão 10, mas pode ser especificado. Além disso, pode-se especificar um caracter de prefixo"""

        messages = await ctx.channel.history(limit=num_messages).flatten()
        for i in range(1, len(messages)):
            if messages[i].content[0] == prefix:
                await messages[i].delete()

    @clearcm.error
    async def clearcm_error(self, ctx, error):
        if isinstance(error, NotFound): 
            print('All messages in the channel were deleted already.')
        else:
            print(error)
            await ctx.send(f'Eu não possuo permissão para deletar mensagens.')

def setup(bot):
    bot.add_cog(Admin(bot))
