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
    async def test(self, ctx):
        await ctx.send('target')
        print('-'*10 + 'textchannel'+ '-'*10)
        print(self.bot.user.id)
        channel = ctx.channel
        async for message in channel.history(limit=10):
            if self.bot.user.id == message.author.id:
                await message.add_reaction('\U0001f44d')
                break


def setup(bot):
    bot.add_cog(AmongUsRankCog(bot))
