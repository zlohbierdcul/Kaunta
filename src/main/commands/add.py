import discord
from discord.ext import commands
from controller.add_controller import handle_add

class Add(commands.Cog):
    @commands.command()
    async def add2(self, ctx):
        await handle_add(bot=self, interaction=ctx)

async def setup(bot):
    await bot.add_cog(Add(bot))