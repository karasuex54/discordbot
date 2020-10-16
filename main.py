import discord
from discord.ext import tasks

# API Key
inifile = configparser.ConfigParser()
inifile.read('../../config.ini', 'UTF-8')

# Discord Bot
TOKEN = inifile.get('Discord', 'Token')
DEVELOPER_ID = int(inifile.get('Discord', 'Developer_id'))
CHANNEL_ID = int(inifile.get('Discord', 'Channel_id'))

JST = timezone(timedelta(hours=+9), 'JST')
notification_time = ''

client = discord.Client()

# loop 処理
@tasks.loop(seconds=1)
async def test():
    global JST,notification_time
    now = datetime.now(JST)
    now_epoch_second = int(now.timestamp())
    yes = now_epoch_second - 86401
    now = now.strftime('%H:%M')
    if now == notification_time:
        notification_time = ''
        channel_list = await sa.get_channel()
        for channel_id in channel_list:
            cha = client.get_channel(int(channel_id.channel_id))
            user_list = await sa.get_user(channel_id.channel_id)
            for user in user_list:
                await cha.send(user.user_id)
    elif now != '21:46':
        notification_time = '21:46'
# Login
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    test.start()


@client.event
async def on_message(message):

    # Not bot loop
    if message.author == client.user:
        return
    
    mes = list(message.content.split())
    cha = message.channel
    author_id = message.author.id
    channel_id = message.channel.id

    # Basic
    if mes[0] == '$close' and author_id == DEVELOPER_ID:
        await cha.send('Good Bye.')
        await client.close()
    elif mes[0] == '$debug':
        await cha.send(notification_time)

    # submission_atcoder app
    if mes[0] == '$sa':
        if mes[1] == 'insert':
            if len(mes) == 2: return
            await sa.insert_user_submission(mes[2])
            await cha.send('complete')
        elif mes[1] == 'set':
            if len(mes) == 2: return
            if mes[2] == 'channel':
                res = await sa.insert_channel(channel_id)
                await cha.send(res)
            elif mes[2] == 'user' and len(mes) == 4:
                res = await sa.insert_user(mes[3], channel_id)
                await cha.send(res)
        if mes[1] == 'get':
            res = await sa.get_submission('karasuex54',0)
            for i,r in enumerate(res):
                if i>5:break
                print(r)

client.run(TOKEN)
