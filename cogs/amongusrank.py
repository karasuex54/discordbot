import discord
from discord.ext import commands, tasks


class AmongUsRankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_reaction.start()

    @tasks.loop(seconds = 10.0)
    async def check_reaction(self):
        print('tasks.loop')

    @check_reaction.before_loop
    async def before_check_reaction(self):
        await self.bot.wait_until_ready()

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

    @aurc.command()
    async def invite(self, ctx):
        embed = discord.Embed(title='among us やる人募集！', color=0x51ED39)
        embed.add_field(name='VoiceChannel', value='alive-A', inline=True)
        embed.add_field(name='maked by', value=ctx.author.name)

        msg = await ctx.send(embed=embed)

        await msg.add_reaction('\U00002705')
        await msg.add_reaction('\U0001F53C')
        await msg.add_reaction('\U0000274C')

def setup(bot):
    bot.add_cog(AmongUsRankCog(bot))
