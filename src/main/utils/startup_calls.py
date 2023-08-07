# other 
import discord
import sys
import loguru

# custom components
from components.counter_component import get_counter_by_show_id

# config
import config.bot_config as cfg

# logger
from utils.logger import get_logger
logger = get_logger("utils.startup_calls")

# reloads all counter messages
async def reload_counter(bot):
    channel = bot.get_channel(cfg.CHANNEL_ID)
    history = channel.history(limit=100)
    messages = [message async for message in history]
    messages.reverse()
    for message in messages:
        view = discord.ui.View.from_message(message)
        try:
            show_id = view.children[0].custom_id if view.children[0].custom_id.isnumeric() else None
            if show_id != None:
                embed, view = get_counter_by_show_id(show_id=show_id)
                await channel.send(embed=embed, view=view)
        except IndexError as ie:
            logger.info("Message has no view")
        await message.delete()


# loads commands from the commands folder and slash commands
async def load_commands(bot):
    for file in cfg.CMDS_DIR.glob("*.py"):
        cmd_file = "commands." + file.name[:-3]
        try:
            logger.info(f"Loading {cmd_file} ...")
            await bot.load_extension(cmd_file)
            
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            logger.warning(f"Failed to load cog {cmd_file}\n\t{exc}")
    try:
        synched = await bot.tree.sync()
        logger.info(f"Synched {len(synched)} commands")
    except Exception as e:
        logger.error(e)