from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import View
import discord


class Search(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @ui.slash.command(name="Test", guild_ids=[1056612436033155153])
    async def search(self, ctx: Context):
        print("search")
        await ctx.send(f"Search:", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Search(bot))