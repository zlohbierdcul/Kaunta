from typing import Any
import discord
from components.select_menu import ShowSelectMenu
from engine.search_engine import find_show, find_season, find_episodes
from discord.ui import View

async def handle_search(bot, interaction: discord.Interaction, input: str):
    results = find_show(input)
    if (len(results) > 0):
        select_options =  [discord.SelectOption(label=x[0][:100], value=x[1][:100]) for index,x in enumerate(results)][:25]
        select_menu = ShowSelectMenu("Your results..", 1, select_options, False)
        embeded = discord.Embed(title="Results", description=f"Showing only the {len(select_options)} first results!\nPlease select one!", color=discord.Color.from_rgb(0,255,0))
        view = View()
        view.add_item(select_menu)
        await interaction.response.send_message(embed=embeded, view=view)
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Noting", description="I found absolutely noting. \nPlease try again!", color=discord.Color.from_rgb(255,0,0)), delete_after=5)
    
    
