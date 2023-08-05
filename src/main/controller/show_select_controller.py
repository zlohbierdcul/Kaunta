import discord
import glob
import pathlib
from typing import Sequence
from components.counter_component import create_counter_by_show_id


async def handle_show_select(bot, interaction: discord.Interaction, user_id: int, show_id: int):
    embed, view = create_counter_by_show_id(show_id=show_id)
    await interaction.response.send_message(embed=embed, view=view)


def show_exists(des_show):
    current_directory = pathlib.Path(__file__).parent.absolute()
    files = glob.glob(str(current_directory) + "/../resources/*")
    
    for file in files:
        file_name = file.removeprefix(str(current_directory) + "/../resources\\").removesuffix(".json")
        if des_show == file_name:
            return True
    return False




    