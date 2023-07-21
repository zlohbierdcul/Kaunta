from typing import Any
import discord
import typing

async def handle_search(interaction: discord.Interaction, input):
    print("search")
    await interaction.response.send_message(f"Search: {input}", ephemeral=True)