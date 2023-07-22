from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import View
import discord


class Search(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    
    @commands.command()
    async def search2(self, ctx: Context, *search: str):
        await ctx.send(search)

async def setup(bot):
    await bot.add_cog(Search(bot))