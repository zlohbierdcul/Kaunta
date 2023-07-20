import discord
from discord.ext import commands


class Util(commands.Cog):
    @commands.command()
    async def clear(self, ctx):
        await ctx.channel.purge()

async def setup(bot):
    await bot.add_cog(Util(bot))