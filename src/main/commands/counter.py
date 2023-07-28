import discord
from discord.ext import commands
from discord.ext.commands import Context
from components.show_select_component import create_show_select_view


class Counter(commands.Cog):
    @commands.command()
    async def add(self, ctx: Context):
       view = create_show_select_view(ctx.author.id, 1)
       embed = discord.Embed(color=discord.Color.dark_green(), title="Your shows!", description="Please select one of the listed shows!")
       await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Counter(bot))