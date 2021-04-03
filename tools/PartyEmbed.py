from discord import Embed, Colour


class PartyEmbed(Embed):
    def __init__(self, party, description='**Opções:**\n\n:white_check_mark: : Entrar na party\n:x: : Fechar a party (apenas o dono tem essa permissão)\n'):
        super().__init__()

        self.title = ":loudspeaker: " + party['game']
        user = party['owner']

        self = self.set_author(
            name=user.display_name,
            url=Embed.Empty,
            icon_url=user.avatar_url
        )

        # Gold colour
        self.colour = Colour.gold()
        self.description = description

        if len(party['joined']) > 0:
            self.description += f'\n**Batatinhas confirmadas:**\n'
            for i, u in enumerate(party['joined']):
                self = self.add_field(name=f'[{i + 1}]', value=u.mention)
