import discord
from discord.ext import commands
import config.bot_config as cfg

class PersistentBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(command_prefix=cfg.PREFIX, intents=intents)
        
    async def on_ready(self):
        print(self.get_channel(cfg.CHANNEL_ID))