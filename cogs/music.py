import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="play", invoke_without_command=True)
    async def play(self, ctx, url: str = None):
        member = ctx.message.author
        voice = member.voice
        voice_channel = voice.channel
        print(voice_channel)
        # voiceChannel = discord.utils.find(ctx.guild.voice_channels, name=ctx.author.voice_channels)
        # vc = discord.utils.find(lambda x: x.name == str(ctx.author.voice_channels), ctx.guild.voice_channels)
        # await vc.connect()

        # if ctx.author.voice:
        #     voice_channel = ctx.message.author.voice.voice_channel
        #     await self.bot.join_voice_channel(voice_channel)
        # else:
        #     await ctx.send("You must be in a specific voice channel.")

def setup(bot):
    bot.add_cog(Music(bot))