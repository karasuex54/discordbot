import discord
from discord.ext import commands

import mytoken as mt

TOKEN_KEY = mt.token_key()
DEVELOPER_ID = mt.developer_id()

INITIAL_EXTENSIONS = [
    'cogs.testcog'
]

class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print('-'*10)
        print(self.user.name)
        print(self.user.id)
        print('-'*10)

if __name__ == '__main__':
    bot = MyBot(command_prefix='$')
    bot.run(TOKEN_KEY)