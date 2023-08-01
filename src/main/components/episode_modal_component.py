from typing import Any, Coroutine, Optional
from discord.interactions import Interaction
from discord.ui import Modal
import discord
from discord.utils import MISSING

class SetEpisodeModal(Modal):
    def __init__(self, *, min: int, max: int, title: str = "Please enter the episode.", timeout: float | None = None, custom_id: str = ...) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        
    def on_submit(self, interaction: Interaction) -> Coroutine[Any, Any, None]:
        return super().on_submit(interaction)
    
    def on_error(self, interaction: Interaction, error: Exception) -> Coroutine[Any, Any, None]:
        return super().on_error(interaction, error) 