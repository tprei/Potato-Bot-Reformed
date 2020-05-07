from discord import Embed, Colour
from pytz import timezone

class GoldEmbed(Embed):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.id = message.id

        url = message.jump_url
        content = message.content

        # Gold colour
        self.colour = Colour.gold()
        self.description = f'[Ver a mensagem]({url})\n{content}'

        self = self.set_author(
                name=message.author.display_name,
                url=Embed.Empty,
                icon_url=message.author.avatar_url
        )

        creation_date = message.created_at.astimezone(timezone('Etc/GMT+6'))

        timestamp = creation_date.strftime("%d/%m/%Y, %H:%M:%S")
        self = self.set_footer(text=timestamp)
