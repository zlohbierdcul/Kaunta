from typing import Any
import discord
from components.select_menu import ShowSelectMenu
from components.abort_button_component import AbortButton
from engine.search_engine import find_show, find_season, find_episodes
from discord.ui import View

async def handle_search(bot, interaction: discord.Interaction, input: str):
    interaction.response.defer()
    results = find_show(input)
    if (len(results) > 0):
        for index,x in enumerate(results):
            print(f"{index}:: value -- {x[1]} || len -- {len(x[1])}")
        select_options =  [discord.SelectOption(label=x[0][:100], value=x[1][:100]) for index,x in enumerate(results)][:25]
        select_menu = ShowSelectMenu("Your results..", 1, select_options, False)
        abort_button = AbortButton()
        embeded = discord.Embed(title="Results", description=f"Showing only the {len(select_options)} first results!\nPlease select one!", color=discord.Color.from_rgb(0,255,0))
        view = View(None)
        view.add_item(select_menu)
        view.add_item(abort_button)
        await interaction.response.send_message(embed=embeded, view=view)
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Noting", description="I found absolutely noting. \nPlease try again!", color=discord.Color.from_rgb(255,0,0)), delete_after=5)
    
    
