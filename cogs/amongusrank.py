import discord
from discord.ext import commands


class AmongUsRankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None
    
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
        mes = None
        async for message in channel.history(limit=10):
            if self.bot.user.id == message.author.id:
                await message.add_reaction('\U0001f44d')
                mes = message
                break
        print(mes.content)
        self.message_id = mes.id
        print(self.message_id)

    @aurc.command()
    async def check(self, ctx):
        if self.message_id is None:
            await ctx.send('$aurc test を実行してください。')
            return
        message = await ctx.fetch_message(self.message_id)
        for react in message.reactions:
            users = await react.users().flatten()
            for user in users:
                print(user.name, end=" ")
            print()


def setup(bot):
    bot.add_cog(AmongUsRankCog(bot))
