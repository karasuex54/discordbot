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
        voice_channel_all = ctx.guild.voice_channels
        for channel in voice_channel_all:
            channel_name = channel.name
            if len(channel_name) <2:continue
            if channel_name[-2:] == '-A':
                print(channel.name,channel.id)

def setup(bot):
    bot.add_cog(AmongUsRankCog(bot))
