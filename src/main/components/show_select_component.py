from typing import Any, Coroutine, List, Optional, Union
from discord.components import SelectOption
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
from discord.ui import Button, Select, View
from discord.utils import MISSING
from discord import ButtonStyle
from database.database_connection import get_shows_from_user
from controller.show_select_controller import handle_show_select
from components.abort_button_component import AbortButton

global current_page

class BackButton(Button):
    def __init__(self, disabled: bool = False):
        super().__init__(style=ButtonStyle.primary, emoji="◀️", disabled=disabled, row=1)
        self.disabled = True if current_page < 2 else False
        
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        global current_page
        await interaction.message.edit(view=create_show_select_view(interaction.user.id, current_page - 1))
        await interaction.response.defer()
        
        
class ForwardButton(Button):
    def __init__(self, disabled: bool = False):
        super().__init__(style=ButtonStyle.primary, emoji="▶️", disabled=disabled, row=1)
        self.disabled = False if current_page <= int(len(options)/25) else True
        
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        global current_page
        await interaction.message.edit(view=create_show_select_view(interaction.user.id, current_page + 1))
        await interaction.response.defer()
        

class ShowSelect(Select):
    def __init__(self, placeholder: str  = None, options: List[SelectOption] = ...) -> None:
        super().__init__(placeholder=placeholder, options=options)

    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
        show_id = int(list(interaction.data.values())[0][0])
        print(interaction)
        user_id = interaction.user.id
        await handle_show_select(interaction, user_id, show_id)
        await interaction.message.delete()
        

def create_show_select_view(user: int, page: int) -> View:
    shows = get_shows_from_user(user)
    print(f"shows: {shows} , {len(shows)}")
    global options
    global show_select
    global current_page
    current_page = page
    options = [SelectOption(label=x[0], value=x[1], description=f"{x[2]} | {x[3]}") for x in shows]
    x = 25*(page-1)
    y = 25*page
    print(f"x: {x}, y: {y}")
    show_select = ShowSelect("Your shows", options[x:y])
    back_button = BackButton()
    forward_button = ForwardButton()
    abort_button = AbortButton()
    view = View()
    view.add_item(show_select)
    if len(options == 0):
        return None
    if len(options) > 25:
        view.add_item(back_button)
        view.add_item(forward_button)
    view.add_item(abort_button)
    return view