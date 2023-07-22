import discord
from discord import ui
from discord.ext import commands
from controller.reaction_controller import handle_reaction
from controller.message_controller import handle_message
from controller.search_input_controller import handle_search
from discord import app_commands
import config.bot_config as cfg

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=cfg.PREFIX, help_command=None, intents=intents)

@bot.event
async def on_raw_reaction_add(payload):
    await handle_reaction(payload, bot)

@bot.event
async def on_message(message):
    await handle_message(message, bot)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(cfg.STATUS))
    
    for file in cfg.CMDS_DIR.glob("*.py"):
        cmd_file = "commands." + file.name[:-3]
        try:
            print(f"Loading {cmd_file} ...")
            await bot.load_extension(cmd_file)
            
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(cmd_file, exc))
            
    try:
        synched = await bot.tree.sync()
        print(f"Synched {len(synched)} commands")
    except Exception as e:
        print(e)
    print("I'm ready!")
            
@bot.tree.command(name="search")
@app_commands.describe(show="Show to search for.")   
async def search(interaction: discord.Interaction, show: str):
    await handle_search(bot, interaction, show)
    
bot.run(cfg.TOKEN)