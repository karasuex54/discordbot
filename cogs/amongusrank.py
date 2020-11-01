import discord
from discord.ext import commands, tasks


class AmongUsRankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_reaction.start()
        self.message_id = None

    def get_channel_and_message_all(self):
        return [self.message_id]

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
    async def invite(self, ctx):
        await ctx.send('@everyone')
        embed = discord.Embed(title='among us やる人募集！', description='下のリアクションを押してね', color=0x51ED39)
        embed.add_field(name='VoiceChannel', value='alive-A', inline=True)
        embed.add_field(name='maked by', value=ctx.author.name, inline=True)
        embed.add_field(name='参加可能 \U00002705', value='0 人 :', inline=False)
        embed.add_field(name='参加不可 \U0000274C', value='0 人 :', inline=False)
        embed.add_field(name='ワンチャン \U0001F53C', value='0 人 :', inline=False)

        msg = await ctx.send(embed=embed)
        self.message_id = msg.id

        await msg.add_reaction('\U00002705')
        await msg.add_reaction('\U0000274C')
        await msg.add_reaction('\U0001F53C')

    @aurc.command()
    async def test(self, ctx):
        msg = await ctx.fetch_message(self.message_id)
        #channel = self.bot.get_channel(634851862146842654)
        #msg = await channel.fetch_message(772258622934876160)

        rm = [] # reacted members list
        for reaction in msg.reactions:
            if reaction.emoji in ['\U00002705', '\U0000274C', '\U0001F53C']:
                members = []
                print(reaction.emoji)
                async for user in reaction.users():
                    if not (user.bot):
                        print(user)
                        members.append(user.name)
                        await msg.remove_reaction(reaction.emoji, user)
                rm.append(members)
        
        embed = discord.Embed(title='among us やる人募集！', description='下のリアクションを押してね', color=0x51ED39)
        embed.add_field(name='VoiceChannel', value='alive-A', inline=True)
        embed.add_field(name='maked by', value=ctx.author.name, inline=True)
        embed.add_field(name='参加可能 \U00002705', value='{} 人 :{}'.format(len(rm[0]),', '.join(rm[0])), inline=False)
        embed.add_field(name='参加不可 \U0000274C', value='{} 人 :{}'.format(len(rm[1]),''.join(rm[1])), inline=False)
        embed.add_field(name='ワンチャン \U0001F53C', value='{} 人 :{}'.format(len(rm[2]),''.join(rm[2])), inline=False)
        await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(AmongUsRankCog(bot))
