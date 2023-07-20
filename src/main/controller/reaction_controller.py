from config.bot_config import CHANNEL_ID
from discord import RawReactionActionEvent
from discord.ext.commands import Bot

async def handle_reaction(payload: RawReactionActionEvent, bot: Bot):
    if (payload.channel_id != CHANNEL_ID):
        print("wrong channel")
        return
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    await message.remove_reaction(payload.emoji, payload.member)
    print("removed..")