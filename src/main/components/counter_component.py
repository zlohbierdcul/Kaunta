from typing import Any, Coroutine, Optional, Union
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
from discord.ui import Button, View
from database.database_connection import get_show_by_show_id, get_linked_show, get_episode_data, increment_current_ep, decrement_current_ep, increment_current_se, decrement_current_se
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
    def __init__(self, user_id: int, show_id: int, custom_id: str, disabled: bool = False):
        super().__init__(user_id=user_id, show_id=show_id, style=discord.ButtonStyle.primary, emoji="🔼", row=1, disabled=disabled, custom_id=custom_id)
        self.custom_id = str(show_id)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            increment_current_ep(self.show_id)
            view, title, episode_name, current_ep, total_ep, color = create_counter_view(self.show_id)
            embed = create_counter_embed(title, episode_name, current_ep, total_ep, color)
            await interaction.message.edit(embed=embed, view=view)
            await interaction.response.defer()
        
        
class DecrementEpButton(CounterButton):
    def __init__(self, user_id: int, show_id: int, custom_id: str, disabled: bool = False):
        super().__init__(user_id=user_id, show_id=show_id, style=discord.ButtonStyle.primary, emoji="🔽", row=1, disabled=disabled, custom_id=custom_id)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            decrement_current_ep(self.show_id)
            view, title, episode_name, current_ep, total_ep, color = create_counter_view(self.show_id)
            embed = create_counter_embed(title, episode_name, current_ep, total_ep, color)
            await interaction.message.edit(embed=embed, view=view)
            await interaction.response.defer()
        
        
class IncrementSeasonButton(CounterButton):
    def __init__(self, user_id: int, show_id: int, custom_id: str, disabled: bool = False, sequel_id: int = None):
        super().__init__(user_id=user_id, show_id=show_id, style=discord.ButtonStyle.primary, emoji="⏫", row=1, disabled=disabled, custom_id=custom_id)
        self.sequel_id = sequel_id
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            embed, view = create_counter_by_show_id(self.sequel_id)
            await interaction.message.edit(embed=embed, view=view)
            await interaction.response.defer()
        
        
class DecrementSeasonButton(CounterButton):
    def __init__(self, user_id: int, show_id: int, custom_id: str, disabled: bool = False, prequel_id: int = None):
        super().__init__(user_id=user_id, show_id=show_id, style=discord.ButtonStyle.primary, emoji="⏬", row=1, disabled=disabled, custom_id=custom_id)
        self.prequel_id = prequel_id
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            embed, view = create_counter_by_show_id(self.prequel_id)
            await interaction.message.edit(embed=embed, view=view)
            await interaction.response.defer()


class LinkButton(Button):
    def __init__(self, url: str, title: str = "Link to Episode"):
        super().__init__(style=discord.ButtonStyle.link, emoji="🎞", row=2, url=url, label=title)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await interaction.response.defer()
        
        
class CounterDeleteButton(CounterButton):
    def __init__(self, user_id: int, custom_id: str,):
        super().__init__(user_id=user_id, style=discord.ButtonStyle.danger, emoji="✖️", row=2, custom_id=custom_id)
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        await super().callback(interaction)
        if (self.allowed):
            await interaction.message.delete()
            await interaction.response.defer()
        

class PersistentCounterViewWrapper(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

class PersistentCounterView(PersistentCounterViewWrapper):
    def __init__(self, *, ep_inc_disabled = None, ep_dec_disabled = None, se_inc_disabled = None, se_dec_disabled = None, link_url: str = None, user_id: int = None, show_id: int = None, sequel_id: int = None, prequel_id: int = None):
        super().__init__()
        args = [ep_inc_disabled, ep_dec_disabled, se_inc_disabled, se_dec_disabled, link_url, user_id, show_id, sequel_id, prequel_id]
        nones = [True for x in args if x == None]
        if all(nones):
            return
        ep_inc_btn = IncrementEpButton(user_id=user_id, show_id=show_id, custom_id="ep_inc_btn", disabled=ep_inc_disabled)
        ep_dec_btn = DecrementEpButton(user_id=user_id, show_id=show_id, custom_id="ep_dec_btn", disabled=ep_dec_disabled)
        se_inc_btn = IncrementSeasonButton(user_id=user_id, show_id=show_id, custom_id="se_inc_btn", disabled=se_inc_disabled, sequel_id=sequel_id)
        se_dec_btn = DecrementSeasonButton(user_id=user_id, show_id=show_id, custom_id="se_dec_btn", disabled=se_dec_disabled, prequel_id=prequel_id)
        # link_btn = LinkButton(url=link_url)
        counter_del_btn = CounterDeleteButton(user_id=user_id, custom_id="counter_del_btn")
    
    
        self.add_item(ep_inc_btn)
        self.add_item(ep_dec_btn)
        self.add_item(se_inc_btn)
        self.add_item(se_dec_btn)
        # self.add_item(link_btn)
        self.add_item(counter_del_btn)
        self.user_id = user_id
        self.show_id = show_id
        self.ep_inc_disabled = ep_inc_disabled
        
        
    async def ep_inc_btn(self, interaction: discord.Interaction, button):
        if (self.is_allowed(interaction.user.id)):
            print("allowed")
            await interaction.response.defer()
        
        
    def is_allowed(self, user_id: int) -> bool:
        allowed = True
        if (self.user_id != user_id):
            allowed = False
        return allowed

       
def CounterView(ep_inc_disab: bool, ep_dec_disab: bool, se_inc_disab: bool, se_dec_disab: bool, link_url: str, user_id: int, show_id: int, sequel_id: int, prequel_id: int):
    view = PersistentCounterViewWrapper() 
    #PersistentCounterView(ep_inc_disabled=ep_inc_disab, ep_dec_disabled=ep_dec_disab, se_inc_disabled=se_inc_disab, se_dec_disabled=se_dec_disab, link_url=link_url, user_id=user_id, show_id=show_id, sequel_id=sequel_id, prequel_id=prequel_id)
    ep_inc_btn = IncrementEpButton(user_id=user_id, show_id=show_id, custom_id="ep_inc_btn", disabled=ep_inc_disab)
    ep_dec_btn = DecrementEpButton(user_id=user_id, show_id=show_id, custom_id="ep_dec_btn", disabled=ep_dec_disab)
    se_inc_btn = IncrementSeasonButton(user_id=user_id, show_id=show_id, custom_id="se_inc_btn", disabled=se_inc_disab, sequel_id=sequel_id)
    se_dec_btn = DecrementSeasonButton(user_id=user_id, show_id=show_id, custom_id="se_dec_btn", disabled=se_dec_disab, prequel_id=prequel_id)
    link_btn = LinkButton(url=link_url)
    counter_del_btn = CounterDeleteButton(user_id=user_id, custom_id="counter_del_btn")


    view.add_item(ep_inc_btn)
    view.add_item(ep_dec_btn)
    view.add_item(se_inc_btn)
    view.add_item(se_dec_btn)
    view.add_item(link_btn)
    view.add_item(counter_del_btn)
    return view


def create_counter_view(show_id: int):
    show = get_show_by_show_id(show_id)
    sequel = get_linked_show(show_id)
    sequel_id = None if len(sequel) == 0 else sequel[0][0]
    user_id = show[0][0]
    title = show[0][1]
    current_ep = show[0][2]
    total_ep = show[0][3]
    prequel_id = show[0][4]
    
    episode = get_episode_data(show_id, current_ep)
    episode_name = episode[0][0]
    filler = episode[0][1]
    url = episode[0][2]
    
    color = discord.Color.dark_gold() if filler else discord.Color.brand_green()
    
    ep_inc_disab = True if current_ep == total_ep else False
    ep_dec_disab = True if current_ep == 1 else False
    se_inc_disab = True if len(sequel) < 1 else False
    se_dec_disab = True if prequel_id == None else False
    view = CounterView(ep_inc_disab, ep_dec_disab, se_inc_disab, se_dec_disab, url, user_id, show_id, sequel_id, prequel_id)
    return (view, title, episode_name, current_ep, total_ep, color)


def create_counter_embed(title, episode_name, current_ep, total_ep, color):
    embed = discord.Embed(title=title, description=f"**Title**\n||```\n{episode_name}\n```||\n**Episode**\n```\n{current_ep} | {total_ep}\n``` ", color=color)
    return embed

def create_counter_by_show_id(show_id: int):
    view, title, episode_name, current_ep, total_ep, color = create_counter_view(show_id)
    embed = create_counter_embed(title, episode_name, current_ep, total_ep, color)
    return (embed, view)