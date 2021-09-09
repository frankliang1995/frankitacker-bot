import discord

from discord.ext import commands
# Role Conversion
class BetterRoles(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return await commands.RoleConverter().convert(ctx, argument)
        except commands.BadArgument:
            role_to_return = discord.utils.find(lambda x: x.name.lower() == argument.lower(), ctx.guild.roles)
            if role_to_return is not None:
                return role_to_return
class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Adding the role to users (only admins or roles with role management)
    @commands.group(name="addrole", invoke_without_command=True, pass_context=True)
    @commands.has_permissions(administrator=True, manage_roles=True)
    async def addRole(self, ctx, member: discord.Member = None, role: BetterRoles=None):
        # Check if the user is specified
        if member is None:
            return await ctx.send("You need to specify the member.")
        # Checks if the role is specified
        if role is None:
            return await ctx.send("You need to specify a role")
        # Checks if the user is not in the specified role
        if role not in member.roles:
            try:
                await member.add_roles(role)
                await ctx.send(f"@everyone {member.name} is now part of {role.name}.")
            except: ctx.send("Something went wrong.")
        else:
            await ctx.send(f"{member.name} is already in {role.name}")
    # Removing the role from users (only admins or roles with role management)
    @commands.group(name="removerole", invoke_without_command=True, pass_context=True)
    async def removeRole(self, ctx, member: discord.Member=None, role: BetterRoles=None):
        # Check if the user is specified
        if member is None:
            return await ctx.send("You need to specify the member.")
        # Checks if a role was typed in
        if role is None:
            return await ctx.send("You need to specify a role")
        # Checks if the user is in the specified role
        if role in ctx.author.roles:
            try:
                await ctx.author.remove_roles(role)
                await ctx.send(f"@everyone {member.name} is no longer a part of {role.name}.")
            except: ctx.send("Something went wrong.")
        else:
            await ctx.send(f"{member.name} was not in {role.name}")
    @addRole.error
    @removeRole.error
    async def role_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Sorry {ctx.message.author}, you do not have permissions to do that!")
    # New members coming into the discord
    async def on_member_join(self, member):
        twitch_sub = discord.utils.find(lambda x: x.name == "Twitch Subscriber", member.guild.roles)
        # Checks if member is a twitch subscriber
        if twitch_sub in member.roles:
            role = discord.utils.find(lambda x: x.name == "Tacker Gang", member.guild.roles)
            member.add_roles(role)

def setup(bot):
    bot.add_cog(Roles(bot))