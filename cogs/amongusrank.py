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

    @aurc.command()
    async def info(self, ctx):
        embed = discord.Embed(title='nice bot', description='Nicest bot there is ever.', color=0xff0000)
        embed.set_author(name='aiueo', icon_url='https://www.4gamer.net/games/534/G053435/20201013054/TN/002.jpg')
        embed.add_field(name='Author', value='<YOUR-USERNAME>')
        embed.add_field(name='Server count', value=f'{len(self.bot.guilds)}')
        embed.add_field(name='Invite', value='[Invite link](<insert your OAuth invitation link here>)')

        await ctx.send(embed=embed)

        channel = ctx.channel
        mes = None
        async for message in channel.history(limit=10):
            if self.bot.user.id == message.author.id:
                await message.add_reaction('\U0001f44d')
                mes = message
                break
        print(mes.content)

def setup(bot):
    bot.add_cog(AmongUsRankCog(bot))
