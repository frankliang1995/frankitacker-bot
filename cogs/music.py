import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="play", invoke_without_command=True)
    async def play(self, ctx, url: str):
        voiceChannel = discord.utils.find(ctx.guild.voice_channels, name=ctx.author.voice_channels)
        await voiceChannel.connect()

def setup(bot):
    bot.add_cog(Music(bot))