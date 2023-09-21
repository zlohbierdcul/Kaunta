from discord.ui import Button
from discord import ButtonStyle, Interaction
from typing import Coroutine, Any

class AbortButton(Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.grey, emoji="❌", row=2)
    
    
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await interaction.message.delete()
        await interaction.response.defer()