import discord
from discord.ext import commands
from discord.ext.commands import Context
# from database.database_connection import get_watching_series_from_user
from config.bot_config import CHANNEL_ID


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def info(self, ctx):
        info_board = discord.Embed(
            title="BotName",
            description="This bot made with xegepa bot template.",
            colour=discord.Colour.red()
        )
        info_board.set_footer(text="BotName")
        info_board.set_author(name="xegepa")
        info_board.add_field(name="Commands", value="Type .help for commands.", inline=True)
        await ctx.send(embed=info_board, delete_after=3)

    @commands.command()
    async def avatar(self, ctx: Context):
        pass
        # result = await get_watching_series_from_user("")
        # output = ""
        # for row in result:
        #     output += f"ID: {row[0]} Name: {row[1]}\n"
        # await ctx.send(output, delete_after=3)

    @commands.command()
    async def help(self, ctx):
        info_board = discord.Embed(
            title="BotName",
            colour=discord.Colour.blue()
        )
        info_board.set_footer(text="BotName")
        info_board.set_author(name="xegepa")
        info_board.add_field(name=".avatar", value="Shows your avatar.", inline=False)
        info_board.add_field(name=".info", value="Info about bot.", inline=False)
        info_board.add_field(name=".coinflip", value="CoinFlip game.", inline=False)
        info_board.add_field(name=".joke", value="Makes a joke.", inline=False)
        info_board.add_field(name=".mirror", value="Bot mirrors your sentence.", inline=False)
        info_board.add_field(name=".giveaway", value='Only who has "Admin" role can use this command.', inline=False)
        info_board.add_field(name=".brokethesentence", value='Brokes the sentence.', inline=False)
        info_board.add_field(name=".lenght", value='Give you info about the sentence.', inline=False)
        info_board.add_field(name=".minecraft", value='Shows your minecraft profile.', inline=False)
        info_board.add_field(name=".writinggame", value='Game for fast writing.', inline=False)
        info_board.add_field(name=".wiki", value='Send you the wiki link of requested thing.', inline=False)
        await ctx.send(embed=info_board, delete_after=3)
        


async def setup(bot):
    await bot.add_cog(Info(bot))