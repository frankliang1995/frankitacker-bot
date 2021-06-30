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

    # Get update from member
    async def on_member_update(self, before, after):
        if before is not after:
            ttv = discord.utils.find(lambda x: x.name == "ttv", after.guild.roles)
            streaming_role = discord.utils.find(lambda x: x.name == "🔴 Streaming", after.guild.roles)
            activity_type = None;
            try:
                activity_type = after.activity.type
            except:
                pass
            # current streaming status
            if activity_type is not discord.ActivityType.streaming:
                if streaming_role in after.roles:
                    print(f"{after.name} has stopped streaming.")
                    await after.remove_roles(streaming_role)
            else:
                # checks if the member has a ttv role
                if ttv in after.roles:
                    if streaming_role not in after.roles:
                        print(f"{after.name} has started streaming.")
                        await after.add_roles(streaming_role)
            # send streaming message
            streaming_channel = discord.utils.find(lambda x: x.name == "streaming", after.guild.channels)
            # checks if the streaming role was recently added to the after member
            if streaming_role in after.roles and streaming_role not in before.roles:
                # sends streaming message to the streaming channel
                stream_message = await streaming_channel.send(f"{after.name} is now live on {after.activity.streaming.platform},\033[3m{'playing'}\033[0m {after.activity.streaming.game}! \n"
                                             f"\n"
                                             f"Title: {after.activity.streaming.name} \n"
                                             f"Url: {after.activity.streaming.url}")
                self.stream_dict[after] = stream_message
            elif streaming_role in before.roles and streaming_role not in after.roles:
                # delete streaming message from channel
                msg = await self.get_message(streaming_channel, self.stream_dict[after])
                await msg.delete()

    # Closes the session
    async def close(self):
        await super().close()
        # await self.session.close()

    def run(self):
        super().run(self.token, reconnect=True)

if __name__ == '__main__':
    frankbot = FrankBot()
    frankbot.run()