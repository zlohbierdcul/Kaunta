import discord
import glob
import pathlib
from components.counter_component import create_counter_view, create_counter_embed


async def handle_show_select(interaction: discord.Interaction, user_id: int, show_id: int):
    view, title, episode_name, current_ep, total_ep, color = create_counter_view(show_id)
    embed = create_counter_embed(title, episode_name, current_ep, total_ep, color)
    await interaction.response.send_message(embed=embed, view=view)


def show_exists(des_show):
    current_directory = pathlib.Path(__file__).parent.absolute()
    files = glob.glob(str(current_directory) + "/../resources/*")
    
    for file in files:
        file_name = file.removeprefix(str(current_directory) + "/../resources\\").removesuffix(".json")
        if des_show == file_name:
            return True
    return False




