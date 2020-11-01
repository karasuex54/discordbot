import discord
from discord.ext import commands, tasks

import models as md

class AmongUs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_reaction.start()

    @tasks.loop(seconds = 10.0)
    async def check_reaction(self):
        print('tasks.loop')
        plans = md.read_plans()
        for plan in plans:
            user_id = int(plan.user_id)
            channel_id = int(plan.channel_id)
            message_id = int(plan.message_id)
            
            user = self.bot.get_user(user_id)
            channel = self.bot.get_channel(channel_id)
            message = await channel.fetch_message(message_id)
            for reaction in message.reactions:
                pass


    @check_reaction.before_loop
    async def before_check_reaction(self):
        await self.bot.wait_until_ready()


    @commands.group()
    async def au(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')

    @au.command()
    async def init(self, ctx):
        guild_id = ctx.guild.id
        channle_id = ctx.channel.id
        
        await ctx.send('bot の発言場所を '+ctx.channel.name+' に設定しました。')

    @au.command()
    async def plan(self, ctx):
        await ctx.send('@everyone')
        embed = discord.Embed(title='among us やる人募集！', description='下のリアクションを押してね', color=0x51ED39)
        embed.add_field(name='VoiceChannel', value='alive-A', inline=True)
        embed.add_field(name='maked by', value=ctx.author.name, inline=True)
        embed.add_field(name='参加可能 \U00002705', value='0 人 :', inline=False)
        embed.add_field(name='参加不可 \U0000274C', value='0 人 :', inline=False)
        embed.add_field(name='ワンチャン \U0001F53C', value='0 人 :', inline=False)

        msg = await ctx.send(embed=embed)

        await msg.add_reaction('\U00002705')
        await msg.add_reaction('\U0000274C')
        await msg.add_reaction('\U0001F53C')

        user_id = ctx.author.id
        channel_id = ctx.channel.id
        message_id = msg.id
        md.create_plan(str(user_id), str(channel_id), str(message_id))


    @au.command()
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
            else:
                async for user in reaction.users():
                    if not (user.bot):
                        await msg.remove_reaction(reaction.emoji, user)
                pass
        
        user_id = 254748747576246272
        user = self.bot.get_user(user_id)

        embed = discord.Embed(title='among us やる人募集！', description='下のリアクションを押してね', color=0x51ED39)
        embed.add_field(name='VoiceChannel', value='alive-A', inline=True)
        embed.add_field(name='maked by', value=user.name, inline=True)
        embed.add_field(name='参加可能 \U00002705', value='{} 人 :{}'.format(len(rm[0]),', '.join(rm[0])), inline=False)
        embed.add_field(name='参加不可 \U0000274C', value='{} 人 :{}'.format(len(rm[1]),''.join(rm[1])), inline=False)
        embed.add_field(name='ワンチャン \U0001F53C', value='{} 人 :{}'.format(len(rm[2]),''.join(rm[2])), inline=False)
        await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(AmongUs(bot))
