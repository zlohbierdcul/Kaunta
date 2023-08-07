#other
from typing import Any, Coroutine, Optional
from discord.interactions import Interaction
from discord.ui import Modal, TextInput, View
import discord
from discord.utils import MISSING

# components


# Database
from database.database_connection import get_show_by_show_id, set_episode

class SetEpisodeModal(Modal):
    def __init__(self, *,counter_interaction: discord.Interaction, show_id: int,  min: int, max: int, title: str = "Please enter the episode.", timeout: float = None, custom_id: str = "set_ep_btn") -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        text_input = TextInput(label="Set Episode of .. Show ..", placeholder="Enter episode number", custom_id="episode_input", max_length=len(str(max)))
        self.add_item(text_input)
        self.counter_interaction = counter_interaction
        self.show_id = show_id
        self.min = min
        self.max = max

        
    async def on_submit(self, interaction: Interaction) -> Coroutine[Any, Any, None]:
        from components.counter_component import get_counter_by_show_id
        try:
            episode_number = int(self.children[0].__str__())
            if self.min <= episode_number <= self.max:
                set_episode(show_id=self.show_id, episode=episode_number)
                embed, view = get_counter_by_show_id(self.show_id)
                await self.counter_interaction.message.edit(embed=embed, view=view)
            else:
                await interaction.response.send_message("Invalid episode number. Please enter a valid number.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Invalid input. Please enter a valid number.", ephemeral=True)
        await interaction.response.defer()