import discord
from discord.ext import commands


class AmongUsRankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def aurc(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')

    @aurc.command()
    async def init(self, ctx):
        guild_id = ctx.guild.id
        voice_channel_id_all = ctx.guild.voice_channels
        for i in voice_channel_id_all:
            print(i.id)

def setup(bot):
    bot.add_cog(AmongUsRankCog(bot))
