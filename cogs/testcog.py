import discord
from discord.ext import commands


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

    @commands.command()
    async def what(self, ctx, what=""):
        await ctx.send(f'{what}とはなんですか？')

    @commands.group()
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')

    @role.command()
    async def test(self, ctx):
        await ctx.send('$role test')
    
    @commands.command(name='list')
    async def _list(self, ctx):
        await ctx.send('$list')

    @commands.command(aliases=['hh'])
    async def hogehoge(self, ctx):
        await ctx.send('$hogehoge or $hh')

def setup(bot):
    bot.add_cog(TestCog(bot))
