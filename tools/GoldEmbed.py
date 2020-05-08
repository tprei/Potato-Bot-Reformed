from discord import Embed, Colour
from pytz import timezone
from utils.helper import isimage

def is_simple(attachments):
    return len(attachments) == 0 or (len(attachments) == 1 and isimage(attachments[0].filename))

class GoldEmbed(Embed):
    def __init__(self, message):
        super().__init__()

        self.simple = False

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

        attachments = message.attachments

        if is_simple(attachments):
            if len(attachments) == 1 and isimage(attachments[0].filename):
                image_url = attachments[0].url
                self = self.set_image(url=image_url)
            self.simple = True

        creation_date = message.created_at.astimezone(timezone('Etc/GMT+6'))

        timestamp = creation_date.strftime("%d/%m/%Y, %H:%M:%S")
        self = self.set_footer(text=timestamp)
