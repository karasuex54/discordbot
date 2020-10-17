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
            if len(channel_name) < 2:continue
            if channel_name[-2:] == '-':
                print(channel.name,channel.id)
        channel_id = 766689793521352734
        voice_channel = self.bot.get_channel(channel_id)
        print("----- voice_channel info -----")
        for mem in voice_channel.members:
            print(mem)

def setup(bot):
    bot.add_cog(AmongUsRankCog(bot))
