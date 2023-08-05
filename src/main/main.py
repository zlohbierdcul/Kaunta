### Imports ###
# other
import discord

from discord import app_commands
from pprint import pprint as pp



# custom components
from components.persistent_bot_component import PersistentBot
from components.counter_component import create_counter_by_show_id

# controller handler
from controller.search_input_controller import handle_search
from controller.add_controller import handle_add
from controller.message_controller import handle_message
from controller.reaction_controller import handle_reaction

# data
import config.bot_config as cfg

# util
from utils.startup_calls import reload_counter, load_commands
from utils.logger import get_logger

### Logging
logger = get_logger("main")


### Bot Startup ###
logger.info("Bot setup")
bot = PersistentBot()


### Bot Event Callbacks
@bot.event
async def on_raw_reaction_add(payload):
    await handle_reaction(payload, bot)


@bot.event
async def on_message(message):
    await handle_message(message, bot)


@bot.event
async def on_ready():
    await reload_counter(bot)
    await load_commands(bot)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(cfg.STATUS))
    logger.info(f"Bot ready in CHANNEL: {cfg.CHANNEL_ID}")
    

### Slash-Commands ###
@bot.tree.command(name="add")
async def add(interaction: discord.Interaction):
    await handle_add(bot, interaction)
            
@bot.tree.command(name="search")
@app_commands.describe(show="Show to search for.")   
async def search(interaction: discord.Interaction, show: str):
    await handle_search(bot, interaction, show)

### Start Bot!! ###
bot.run(cfg.TOKEN)