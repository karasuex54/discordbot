from datetime import datetime
from time import time

import discord
import models as md
import mytoken as mt
from discord.ext import commands, tasks


class AmongUs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = mt.amongus_guild_id()
        self.role_names = ['BEGINNER','BRONZE','SILVER','GOLD']
        self.plan_stumps = ['\U00000030\U0000FE0F\U000020E3', '\U00000031\U0000FE0F\U000020E3', '\U00000032\U0000FE0F\U000020E3', '\U00000033\U0000FE0F\U000020E3', '\U00000034\U0000FE0F\U000020E3', '\U0001F53C', '\U0000274C']

    def is_notice_in_guild_id(self, guild_id):
        for notice in md.read_notices():
            if guild_id == notice.guild_id:
                return True, notice.channel_id
        return False, ''


    def is_reactions_by_user_channel_message(self, user_id, channel_id, message_id):
        for reaction in md.read_reactions():
            if [reaction.user_id, reaction.channel_id, reaction.message_id] == [user_id, channel_id, message_id]:
                return True
        return False


    def get_reaction_members(self, channel_id, message_id):
        members = [[] for i in range(len(self.plan_stumps))]
        for r in md.read_reactions():
            if [r.channel_id, r.message_id] == [channel_id, message_id]:
                members[self.plan_stumps.index(r.stump)].append(self.bot.get_user(int(r.user_id)).name)
        return members

    def make_plan(self, author_id, members, epoch_time):
        dt = datetime.fromtimestamp(epoch_time)
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
        for plan in md.read_plans():
            channel_id,message_id = plan.channel_id,plan.message_id
            channel = self.bot.get_channel(int(channel_id))
            message = await channel.fetch_message(int(message_id))
            for reaction in message.reactions:
                if reaction.emoji in self.plan_stumps:
                    if reaction.count == 1:
                        continue
                    async for user in reaction.users():
                        if user.bot:
                            continue
                        else:
                            is_created = self.is_reactions_by_user_channel_message(str(user.id), channel_id, message_id)
                            if is_created:
                                md.update_reaction(reaction.emoji, str(user.id), channel_id, message_id)
                            else:
                                md.create_reaction(reaction.emoji, str(user.id), channel_id, message_id)
                            await message.remove_reaction(reaction.emoji, user)
                else:
                    await reaction.clear()
            members = self.get_reaction_members(channel_id, message_id)
            embed = self.make_plan(plan.user_id, members, plan.epoch_time)
            await message.edit(embed=embed)


    def is_member_in_timecounts(self, user_id):
        for timecount in md.read_timecounts():
            if timecount.user_id == user_id:
                return (True, timecount.time_counts)
        return (False, 0)


    async def count_time_in_voice_channel(self):
        print('count_time_in_voice_channel')
        for notice in md.read_notices():
            for vc in self.bot.get_guild(int(notice.guild_id)).voice_channels:
                if len(vc.members) < 3:continue
                for user in vc.members:
                    if self.is_member_in_timecounts(str(user.id))[0]:
                        md.update_timecounts(str(user.id), 5)
                    else:
                        md.create_timecounts(str(user.id))


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
        for notice in md.read_notices():
            guild = self.bot.get_guild(int(notice.guild_id))
            roles = {}
            for role in guild.roles:
                if role.name in self.role_names:
                    roles[role.name] = role
            if roles == {}:
                continue
            for user in guild.members:
                r,tc = self.is_member_in_timecounts(str(user.id))
                if tc == 0:
                    continue
                rt = self.role_threshold(tc)
                if rt[0]:
                    await user.remove_roles(roles[rt[0]])
                await user.add_roles(roles[rt[1]])



    @tasks.loop(seconds = 5.0)
    async def loop_function(self):
        await self.count_time_in_voice_channel()
        await self.update_plan()
        await self.give_role()


    @loop_function.before_loop
    async def before_loop_function(self):
        await self.bot.wait_until_ready()


    @commands.group()
    async def au(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')


    @au.command()
    async def init(self, ctx):
        guild_id = str(ctx.guild.id)
        channel_id = str(ctx.channel.id)
        is_notice,c = self.is_notice_in_guild_id(guild_id)
        if is_notice:
            md.update_notice(guild_id, channel_id)
        else:
            md.create_notice(guild_id, channel_id)
        await ctx.send('bot の発言場所を '+ctx.channel.name+' に設定しました。')


    @au.command()
    async def plan(self, ctx):
        guild_id = str(ctx.guild.id)
        is_notice,channel_id = self.is_notice_in_guild_id(guild_id)
        if is_notice:
            channel = self.bot.get_channel(int(channel_id))
            user_id = str(ctx.author.id)
            embed = self.make_plan(user_id, [[] for i in range(len(self.plan_stumps))])
            msg = await channel.send(embed=embed)
            for stump in self.plan_stumps:
                await msg.add_reaction(stump)
            message_id = str(msg.id)
            md.create_plan(user_id, channel_id, message_id)
        else:
            await ctx.send('plz "$au notice"')


    @au.command()
    async def test(self, ctx):
        pass


def setup(bot):
    bot.add_cog(AmongUs(bot))
