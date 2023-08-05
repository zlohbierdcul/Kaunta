import discord
from components.show_select_component import create_show_select_view
from typing import Sequence

async def handle_add(bot, interaction: discord.Interaction):
    view = create_show_select_view(bot, interaction.user.id, 1)
    if (view != None):
        embed = discord.Embed(color=discord.Color.dark_green(), title="Your shows!", description="Please select one of the listed shows!")
        await interaction.response.send_message(embed=embed, view=view)
    else:
        embed = discord.Embed(color=discord.Color.dark_green(), title="No shows!", description="No shows have been added jet!\nType \n`\n/search\`\n [and the show you want to search for] to get started!")
        await interaction.response.send_message(embed=embed, delete_after=5)
        
