from config.bot_config import CHANNEL_ID
from discord import Message
from discord.ext.commands import Bot

async def handle_message(message: Message, bot: Bot):
    if (message.channel.id != CHANNEL_ID):
        return
    # TODO: check if author is bot before deleting
    if (message.author.id != bot.shard_id):
        await message.delete(delay=1)
        await bot.process_commands(message)
