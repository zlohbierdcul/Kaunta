import discord
from discord import Embed
from discord.ui import View, Button
from engine.search_engine import find_season, find_episodes
from database.database_connection import show_exists_for_user, add_episodes_to_show
from pprint import pprint as pp
from components.abort_button_component import AbortButton

class ShowSelectMenu(discord.ui.Select):
    options = []
    disabled = False
    placeholder = "Choose a show!"
    max_values = 0

    def __init__(self, placeholder, max_values, options, disabled):
        super().__init__(placeholder=placeholder, min_values=1, max_values=max_values, options=options, disabled=disabled)


    async def callback(self, interaction: discord.Interaction):
        
        selected_show = list(interaction.data.values())[0][0]
        print(f"selected_show: {selected_show}")
        seasons = find_season(selected_show)
        print(f"seasons: {seasons}")
        
        if (len(seasons) > 1):
            embeded = discord.Embed(title="Results", description="Showing only the 25 first results!\nPlease select one or more!", color=discord.Color.from_rgb(0,255,0))
            select_options =  [discord.SelectOption(label=x[0][:100], value=x[1][:100]) for index,x in enumerate(seasons)][:25]
            select_menu = SeasonSelectMenu("Your results..", len(select_options), select_options, False)
            abort_button = AbortButton()
            view = View(timeout=None)
            view.add_item(select_menu)
            view.add_item(abort_button)
            await interaction.message.delete()
            await interaction.response.send_message(embed=embeded, view=view)
        else:
            print(f"else: seasons: {seasons}")
            await handle_season_select(interaction, [seasons[0][1]])
        
        
class SeasonSelectMenu(discord.ui.Select):
    options = []
    disabled = False
    placeholder = "Choose a Season!"
    max_values = 0

    def __init__(self, placeholder, max_values, options, disabled):
        super().__init__(placeholder=placeholder, min_values=1, max_values=max_values, options=options, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        await handle_season_select(interaction, list(interaction.data.values())[0])
        

async def handle_season_select(select_interaction: discord.Interaction, season_links: list):
    # Define Callback functions for buttons
    async def yes_add_button_callback(interaction: discord.Interaction):
        watch_links = season_links
        await interaction.message.edit(embed=Embed(color=discord.Color.dark_grey(), title="Please stand-by!", description="Your show/s are currently being processed, this can take a second!"), view=None)
        await handle_show_add(interaction, watch_links)

    async def no_add_button_callback(interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.response.defer()
    
    # Prepare Buttons and View
    yes_add_button = Button(label="Yes", style=discord.ButtonStyle.green)
    yes_add_button.callback = yes_add_button_callback
    no_add_button = Button(label="No", style=discord.ButtonStyle.red)
    no_add_button.callback = no_add_button_callback
    # Add buttons to view
    view = View(timeout=None)
    view.add_item(yes_add_button)
    view.add_item(no_add_button)
    try:
        await select_interaction.message.delete()
    except Exception as e:
        print(e)
    await select_interaction.response.send_message(embed=Embed(title="Add?", description="Do you want to add this to your list?"), view=view)
    
    
async def handle_show_add(interaction: discord.Interaction, watch_links):
    prequel = None
    added_shows = ""
    for show_link in watch_links:
        episodes_json = find_episodes(show_link)
        show_name = list(episodes_json.keys())[0]
        if not show_exists_for_user(show_name, interaction.user.id):
            add_episodes_to_show(episodes_json[show_name], show_name, interaction.user.id, interaction.user.name, prequel)
            prequel = show_name
            added_shows += show_name + ", "
        else:
            await interaction.response.send_message(embed=Embed(title="Show exists already!", description=f"{show_name} already exists for this user. \n Skipping this season/show!", color=discord.Color.from_rgb(222,0,0)), delete_after=6)
    added_shows = added_shows[:-1]
    if len(added_shows) > 0:
        await interaction.channel.send(embed=Embed(title="Show added!", description=f"{added_shows} added!"), delete_after=5)
        await interaction.message.delete()
    
    