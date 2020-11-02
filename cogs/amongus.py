import discord
from discord.ext import commands, tasks

import models as md

class AmongUs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_reaction.start()


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
        members = [[] for i in range(3)]
        stump = ['\U00002705', '\U0001F53C', '\U0000274C']
        for r in md.read_reactions():
            if [r.channel_id, r.message_id] == [channel_id, message_id]:
                members[stump.index(r.reaction)].append(self.bot.get_user(int(r.user_id)).name)
        return members
    
    def make_plan(self,author_id,members):
        embed = discord.Embed(title='among us やる人募集！', description='下のリアクションを押してね', color=0x51ED39)
        embed.add_field(name='maked by', value=self.bot.get_user(int(author_id)).name, inline=True)
        embed.add_field(name='参加可能 \U00002705', value='{} 人 : {}'.format(len(members[0]), ' '.join(members[0])), inline=False)
        embed.add_field(name='ワンチャン \U0001F53C', value='{} 人 : {}'.format(len(members[1]), ' '.join(members[1])), inline=False)
        embed.add_field(name='参加不可 \U0000274C', value='{} 人 : {}'.format(len(members[2]), ' '.join(members[2])), inline=False)
        return embed

    @tasks.loop(seconds = 10.0)
    async def check_reaction(self):
        print('check_reaction')
        for plan in md.read_plans():
            channel_id,message_id = plan.channel_id,plan.message_id
            channel = self.bot.get_channel(int(channel_id))
            message = await channel.fetch_message(int(message_id))
            for reaction in message.reactions:
                async for user in reaction.users():
                    if user.bot:
                        pass
                    else:
                        if reaction.emoji in ['\U00002705', '\U0000274C', '\U0001F53C']:
                            is_created = self.is_reactions_by_user_channel_message(str(user.id), channel_id, message_id)
                            if is_created:
                                md.update_reaction(reaction.emoji, str(user.id), channel_id, message_id)
                            else:
                                md.create_reaction(reaction.emoji, str(user.id), channel_id, message_id)
                        await message.remove_reaction(reaction.emoji, user)
            members = self.get_reaction_members(channel_id, message_id)
            embed = self.make_plan(plan.user_id, members)
            await message.edit(embed=embed)


    @check_reaction.before_loop
    async def before_check_reaction(self):
        await self.bot.wait_until_ready()


    @commands.group()
    async def au(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')


    @au.command()
    async def notice(self, ctx):
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
            #await channel.send('@everyone')
            embed = self.make_plan(user_id, [[],[],[]])
            msg = await channel.send(embed=embed)
            await msg.add_reaction('\U00002705')
            await msg.add_reaction('\U0001F53C')
            await msg.add_reaction('\U0000274C')
            message_id = str(msg.id)
            md.create_plan(user_id, channel_id, message_id)
        else:
            await ctx.send('plz "$au notice"')


    @au.command()
    async def test(self, ctx):
        return


def setup(bot):
    bot.add_cog(AmongUs(bot))