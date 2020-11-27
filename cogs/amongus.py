from datetime import datetime, timedelta, timezone
from time import time

import discord
import models as md
import mytoken as mt
from discord.ext import commands, tasks

JST = timezone(timedelta(hours=+9), 'JST')

class Amongus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = mt.amongus_guild_id()
        self.channel_id = mt.amongus_channel_id()
        self.role_names = ['BEGINNER','BRONZE','SILVER','GOLD']
        self.plan_stumps = ['\U00000030\U0000FE0F\U000020E3', '\U00000031\U0000FE0F\U000020E3', '\U00000032\U0000FE0F\U000020E3', '\U00000033\U0000FE0F\U000020E3', '\U00000034\U0000FE0F\U000020E3', '\U0001F53C', '\U0000274C']

        self.loop_function.start()


    def is_user_reaction_in_plan(self, user_id, message_id):
        for r in md.read_amongus_reactions():
            if [r.user_id, r.message_id] == [user_id, message_id]:
                return True
        return False


    def get_reaction_members(self, message_id):
        members = [[] for i in range(len(self.plan_stumps))]
        for r in md.read_amongus_reactions():
            if r.message_id == message_id:
                members[self.plan_stumps.index(r.stump)].append(self.bot.get_user(int(r.user_id)).name)
        return members

    def make_plan(self, author_id, members, epoch_time):
        dt = datetime.fromtimestamp(epoch_time, JST)
        dt_str = dt.strftime('%m/%d')
        embed = discord.Embed(title=dt_str+' among us やる人募集！', description='下のリアクションを押してね', color=0x56f000)
        embed.add_field(name='made by', value=self.bot.get_user(int(author_id)).name, inline=False)
        embed.add_field(name=self.plan_stumps[0]+' 19:00 から参加可能', value='{} 人 : {}'.format(len(members[0]), ', '.join(members[0])), inline=False)
        embed.add_field(name=self.plan_stumps[1]+' 20:00 から参加可能', value='{} 人 : {}'.format(len(members[1]), ', '.join(members[1])), inline=False)
        embed.add_field(name=self.plan_stumps[2]+' 21:00 から参加可能', value='{} 人 : {}'.format(len(members[2]), ', '.join(members[2])), inline=False)
        embed.add_field(name=self.plan_stumps[3]+' 22:00 から参加可能', value='{} 人 : {}'.format(len(members[3]), ', '.join(members[3])), inline=False)
        embed.add_field(name=self.plan_stumps[4]+' 23:00 から参加可能', value='{} 人 : {}'.format(len(members[4]), ', '.join(members[4])), inline=False)
        embed.add_field(name=self.plan_stumps[5]+' わからない', value='{} 人 : {}'.format(len(members[5]), ', '.join(members[5])), inline=False)
        embed.add_field(name=self.plan_stumps[6]+' 参加不可', value='{} 人 : {}'.format(len(members[6]), ', '.join(members[6])), inline=False)
        return embed


    async def update_plan(self):
        print('update_plan')
        for p in md.read_amongus_plans():
            message_id = p.message_id
            channel = self.bot.get_channel(int(p.channel_id))
            message = await channel.fetch_message(int(message_id))
            for reaction in message.reactions:
                if reaction.emoji in self.plan_stumps:
                    if reaction.count == 1:
                        continue
                    async for user in reaction.users():
                        if user.bot:
                            continue
                        else:
                            is_created = self.is_user_reaction_in_plan(str(user.id), message_id)
                            if is_created:
                                md.update_amongus_reaction(message_id, str(user.id), reaction.emoji)
                            else:
                                md.create_amongus_reaction(message_id, str(user.id), reaction.emoji, int(time()))
                            await message.remove_reaction(reaction.emoji, user)
                else:
                    await reaction.clear()
            members = self.get_reaction_members(message_id)
            embed = self.make_plan(p.author_id, members, p.epoch_time)
            await message.edit(embed=embed)


    def is_user_in_userranks(self, user_id):
        for user_ranks in md.read_amongus_user_ranks():
            if user_ranks.user_id == user_id:
                return (True, user_ranks.time_counts)
        return (False, 0)


    async def count_time_in_voice_channel(self):
        print('count_time_in_voice_channel')
        guild = self.bot.get_guild(int(self.guild_id))
        for vc in guild.voice_channels:
            if len(vc.members) < 3:
                continue
            for user in vc.members:
                user_id = str(user.id)
                if self.is_user_in_userranks(user_id)[0]:
                    md.update_amongus_user_ranks(user_id, 5)
                else:
                    md.create_amongus_user_rank(user_id)


    def role_threshold(self, time_count):
        rank = self.role_names
        if time_count > 18000:
            return (rank[2], rank[3])
        elif time_count > 7200:
            return (rank[1], rank[2])
        elif time_count > 3600:
            return (rank[0], rank[1])
        elif time_count > 0:
            return (False, rank[0])


    async def give_role(self):
        print('give_role')
        guild = self.bot.get_guild(int(self.guild_id))
        roles = {}
        for role in guild.roles:
            if role.name in self.role_names:
                roles[role.name] = role
        for user in guild.members:
            r,tc = self.is_user_in_userranks(str(user.id))
            if tc == 0:
                continue
            rt = self.role_threshold(tc)
            if rt[0]:
                await user.remove_roles(roles[rt[0]])
            await user.add_roles(roles[rt[1]])


    def is_same_day(self, epoch_time):
        today = datetime.fromtimestamp(epoch_time, JST).strftime('%m/%d')
        for p in md.read_amongus_plans():
            day = datetime.fromtimestamp(p.epoch_time, JST).strftime('%m/%d')
            if today == day:
                return True
        return False

    @tasks.loop(seconds = 5.0)
    async def loop_function(self):
        print('loop_function')
        try:
            await self.count_time_in_voice_channel()
            await self.update_plan()
        except:
            pass
        #await self.give_role()


    @loop_function.before_loop
    async def before_loop_function(self):
        await self.bot.wait_until_ready()


    @commands.group()
    async def au(self, ctx):
        if ctx.guild.id != int(self.guild_id):
            await ctx.send('指定されてないサーバーです。')
        elif ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')


    @au.command()
    async def init(self, ctx):
        await ctx.send('au init')


    @au.command()
    async def plan(self, ctx):
        epoch_time = int(time())
        if self.is_same_day(epoch_time):
            return
        channel = self.bot.get_channel(int(self.channel_id))
        author_id = str(ctx.author.id)
        embed = self.make_plan(author_id, [[] for i in range(len(self.plan_stumps))], epoch_time)
        await channel.send('@here')
        msg = await channel.send(embed=embed)
        for stump in self.plan_stumps:
            await msg.add_reaction(stump)
        message_id = str(msg.id)
        md.create_amongus_plan(self.guild_id, self.channel_id, author_id, message_id, epoch_time)



    @au.command()
    async def test(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Amongus(bot))
