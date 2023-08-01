from typing import Any, Coroutine, Optional, Union
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
from discord.ui import Button, View
from database.database_connection import get_show_by_show_id, get_linked_show, get_episode_data, increment_current_ep, decrement_current_ep
import discord

class CounterButton(Button):
    def __init__(self, *, user_id: int, show_id: int = None, style: ButtonStyle = ButtonStyle.secondary, label: str  = None, disabled: bool = False, custom_id: str  = None, url: str  = None, emoji: str = None, row: int  = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
        self.user_id = user_id
        self.show_id = show_id

    async def callback(self, interaction: Interaction) -> Any:
        self.allowed = True
        if (self.user_id != interaction.user.id):
            self.allowed = False

class IncrementEpButton(CounterButton):
    def __init__(self, user_id: int, show_id: int, disabled: bool = False):
        super().__init__(user_id=user_id, show_id=show_id, style=discord.ButtonStyle.primary, emoji="🔼", row=1, disabled=disabled)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            update_database_ep_increment(self.show_id)
            view, title, episode_name, current_ep, total_ep, color = create_counter_view(self.show_id)
            embed = create_counter_embed(title, episode_name, current_ep, total_ep, color)
            await interaction.message.edit(embed=embed, view=view)
            await interaction.response.defer()
        
        
class DecrementEpButton(CounterButton):
    def __init__(self, user_id: int, show_id: int, disabled: bool = False):
        super().__init__(user_id=user_id, show_id=show_id, style=discord.ButtonStyle.primary, emoji="🔽", row=1, disabled=disabled)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            update_database_ep_decrement(self.show_id)
            view, title, episode_name, current_ep, total_ep, color = create_counter_view(self.show_id)
            embed = create_counter_embed(title, episode_name, current_ep, total_ep, color)
            await interaction.message.edit(embed=embed, view=view)
            await interaction.response.defer()
        
        
        
class IncrementSeasonButton(CounterButton):
    def __init__(self, user_id: int, show_id: int, disabled: bool = False):
        super().__init__(user_id=user_id, show_id=show_id, style=discord.ButtonStyle.primary, emoji="⏫", row=1, disabled=disabled)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            await interaction.response.defer()
        
        
class DecrementSeasonButton(CounterButton):
    def __init__(self, user_id: int, show_id: int, disabled: bool = False):
        super().__init__(user_id=user_id, show_id=show_id, style=discord.ButtonStyle.primary, emoji="⏬", row=1, disabled=disabled)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            await interaction.response.defer()


class LinkButton(Button):
    def __init__(self, url: str, title: str = "Link to Episode"):
        super().__init__(style=discord.ButtonStyle.link, emoji="🎞", row=2, url=url, label=title)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        # TODO Implement callback for episode increment
        await interaction.response.defer()
        
        
class CounterDeleteButton(CounterButton):
    def __init__(self, user_id: int):
        super().__init__(user_id=user_id, style=discord.ButtonStyle.danger, emoji="✖️", row=2)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            await interaction.message.delete()
            await interaction.response.defer()
        # TODO Implement callback for episode increment
        
        
def CounterView(ep_inc_disab: bool, ep_dec_disab: bool, se_inc_disab: bool, se_dec_disab: bool, link_url: str, user_id: int, show_id: int):
    view = View()
    view.add_item(IncrementEpButton(user_id, show_id, ep_inc_disab))
    view.add_item(DecrementEpButton(user_id, show_id, ep_dec_disab))
    view.add_item(IncrementSeasonButton(user_id, show_id, se_inc_disab))
    view.add_item(DecrementSeasonButton(user_id, show_id, se_dec_disab))
    view.add_item(LinkButton(link_url))
    view.add_item(CounterDeleteButton(user_id))
    return view


def create_counter_view(show_id: int):
    show = get_show_by_show_id(show_id)
    sequel = get_linked_show(show_id)
    user_id = show[0][0]
    title = show[0][1]
    current_ep = show[0][2]
    total_ep = show[0][3]
    previous = show[0][4]
    
    episode = get_episode_data(show_id, current_ep)
    episode_name = episode[0][0]
    filler = episode[0][1]
    url = episode[0][2]
    
    color = discord.Color.dark_gold() if filler else discord.Color.brand_green()
    
    ep_inc_disab = True if current_ep == total_ep else False
    ep_dec_disab = True if current_ep == 1 else False
    se_inc_disab = True if len(sequel) < 1 else False
    se_dec_disab = True if previous == None else False
    view = CounterView(ep_inc_disab, ep_dec_disab, se_inc_disab, se_dec_disab, url, user_id, show_id)
    return (view, title, episode_name, current_ep, total_ep, color)


def create_counter_embed(title, episode_name, current_ep, total_ep, color):
    embed = discord.Embed(title=title, description=f"**Title**\n||```\n{episode_name}\n```||\n**Episode**\n```\n{current_ep} | {total_ep}\n``` ", color=color)
    return embed


def update_database_ep_increment(show_id: int):
    increment_current_ep(show_id)


def update_database_ep_decrement(show_id: int):
    decrement_current_ep(show_id)