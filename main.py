import discord
from discord.ext import commands
from decouple import config

import copy
import json
import aiohttp

INITIAL_EXTENSIONS = [
    'cogs.roles',
]

class FrankBot(commands.Bot):
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

    # Get update from member
    async def on_member_update(self, before, after):
        if before is not after:
            # current streaming status
            if after.status == "streaming":
                # checks if the member has a ttv role
                ttv = discord.utils.find(lambda x: x.name == "ttv", after.guild.roles)
                if ttv in after.roles:
                    # checks if the member has the streaming role
                    streaming = discord.utils.find(lambda x: x.name == "🔴 Streaming", after.guild.roles)
                    if streaming not in after.roles:
                        # add the user to the streaming
                        after.add_roles(streaming)
            # checks if the streaming role was recently added to the after member
            streaming = discord.utils.find(lambda x: x.name == "🔴 Streaming", after.guild.roles)
            if streaming in after.roles and streaming not in before.roles:
                # sends streaming message to
                streaming_channel = discord.utils.find(lambda x: x.name == "streaming", after.guild.channels)
                # await streaming_channel.send(f"{after.name} is now live on {}")






        # print(after.member.status)

    # Closes the session
    async def close(self):
        await super().close()
        # await self.session.close()

    def run(self):
        super().run(self.token, reconnect=True)

if __name__ == '__main__':
    frankbot = FrankBot()
    frankbot.run()