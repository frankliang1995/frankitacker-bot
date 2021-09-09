import discord

from discord.ext import commands

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="serverinfo", invoke_without_command=True)
    async def serverinfo(self, ctx):
        print(ctx.guild)
        guild_owner = self.bot.get_user(ctx.guild.owner_id)
        print(guild_owner)
        embed = discord.Embed(title="Discord Server Information")
        embed.add_field(name= "SERVER OWNER", value=guild_owner)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Server(bot))