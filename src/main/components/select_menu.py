import discord
from discord import Embed
from discord.ui import View, Button
from engine.search_engine import find_season

class ShowSelectMenu(discord.ui.Select):
    options = []
    disabled = False
    placeholder = "Choose a show!"
    max_values = 0

    def __init__(self, placeholder, max_values, options, disabled):
        super().__init__(placeholder=placeholder, min_values=1, max_values=max_values, options=options, disabled=disabled)


    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        selected_show = list(interaction.data.values())[0][0]
        print(selected_show)
        seasons = find_season(selected_show)
        
        if (len(seasons) > 1):
            embeded = discord.Embed(title="Results", description="Showing only the 25 first results!\nPlease select one or more!", color=discord.Color.from_rgb(0,255,0))
            select_options =  [discord.SelectOption(label=x[0][:100], value=x[1][:100]) for index,x in enumerate(seasons)][:25]
            select_menu = SeasonSelectMenu("Your results..", len(select_options), select_options, False)
            view = View()
            view.add_item(select_menu)
            await interaction.response.send_message(embed=embeded, view=view)
        else:
            await handle_season_select(interaction, list(interaction.data.values())[0])
        
        
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
        print(select_interaction.data["values"])
        await interaction.message.delete()
        await interaction.response.send_message("Ok will be done!", delete_after=3)

    async def no_add_button_callback(interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.response.defer()
    
    # Prepare Buttons and View
    yes_add_button = Button(label="Yes", style=discord.ButtonStyle.green)
    yes_add_button.callback = yes_add_button_callback
    no_add_button = Button(label="No", style=discord.ButtonStyle.red)
    no_add_button.callback = no_add_button_callback
    # Add buttons to view
    view = View()
    view.add_item(yes_add_button)
    view.add_item(no_add_button)
    
    await select_interaction.response.send_message(embed=Embed(title="Add?", description="Do you want to add this to your list?"), view=view)
    
    
    