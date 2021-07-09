import discord
from discord.ext import commands
class Twitch(commands.Cog):
    # key = streaming member, value = message value
    stream_dict = {}
    def __init__(self, bot):
        self.bot = bot
    # Get update from member
    async def on_member_update(self, before, after):
        print("change")
        if before is not after:
            ttv = discord.utils.find(lambda x: x.name == "ttv", after.guild.roles)
            streaming_role = discord.utils.find(lambda x: x.name == "🔴 Streaming Live Now", after.guild.roles)
            activity_type = None
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
                stream_message = await streaming_channel.send(
                    f"{after.name} is now live on {after.activity.streaming.platform},\033[3m{'playing'}\033[0m {after.activity.streaming.game}! \n"
                    f"\n"
                    f"Title: {after.activity.streaming.name} \n"
                    f"Url: {after.activity.streaming.url}")
                self.stream_dict[after] = stream_message
            elif streaming_role in before.roles and streaming_role not in after.roles:
                # delete streaming message from channel
                msg = await self.get_message(streaming_channel, self.stream_dict[after])
                await msg.delete()
def setup(bot):
    bot.add_cog(Twitch(bot))