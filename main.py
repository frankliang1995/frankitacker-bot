import discord
from discord.ext import commands
from decouple import config

import copy
import json
import aiohttp

INITIAL_EXTENSIONS = [
    'cogs.roles',
    'cogs.mods',
    'cogs.twitch',
]

class FrankBot(commands.Bot):
    # key = streaming member, value = message value
    stream_dict = {}
    def __init__(self):
        super().__init__(command_prefix='!',
                         intents=discord.Intents(members=True, presences=True)
                         )
        self.client_id = config('CLIENT_ID')
        self.token = config('TOKEN')

        for extension in INITIAL_EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(
                    extension, type(e).__name__, e))

    # Let us know the bot is ready
    async def on_ready(self):
        # self.session = aiohttp.ClientSession(loop=self.loop)
        print('We have logged in as ' + self.user.name)

    # Gets message from client
    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)
        ctx = await self.get_context(message)
        if ctx.invoked_with and ctx.invoked_with.lower() not in self.commands and ctx.command is None:
            msg = copy.copy(message)
            if ctx.prefix:
                new_content = msg.content[len(ctx.prefix):]
                msg.content = "{}tag get {}".format(ctx.prefix, new_content)
                await self.process_commands(msg)

    # Closes the session
    async def close(self):
        await super().close()
        # await self.session.close()

    def run(self):
        super().run(self.token, reconnect=True)

if __name__ == '__main__':
    frankbot = FrankBot()
    frankbot.run()