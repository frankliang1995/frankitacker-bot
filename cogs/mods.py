import discord
from discord.ext import commands

class Mods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # ----------------- KICK ---------------------------------
    @commands.group("kick", invoke_without_command=True)
    @commands.has_permissions(administrator=True, kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, reason="No Reason Provided."):
        try:
            if ctx.author.top_role > member.top_role:
                await self.kick(member)
                await ctx.send(f"{member} has been kicked. \n"
                               f"Reason: {reason}")
            elif ctx.author.top_role > member.top_role:
                ctx.send(f"{member.display_name} has the same highest role as you.")
            else: ctx.send(f"{member.display_name} has a higher than you.")
        except:
            await ctx.send("Something went wrong")
    @kick.error
    async def kick_error(self, error, ctx):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have kick permissions")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Could not identify target")
        else: raise error
    # ------------------------------------------------------------
    # --------------------BAN_____________________________________
    @commands.group("ban", invoke_without_command=True)
    @commands.has_permissions(administrator=True, ban_members=True)
    async def ban(self, ctx, member: discord.member=None, reason="No Reason Provided"):
        try:
            await self.ban(member)
            await ctx.send(f"{member} has been banned \n"
                           f"Reason: {reason}")
        except:
            await ctx.send("Something went wrong")
    @ban.error
    async def ban_error(self, error, ctx):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have ban permissions")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Coud not identify target")
        else: raise error
    #--------------------------------------------------------------

def setup(bot):
    bot.add_cog(Mods(bot))