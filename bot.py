import discord
from discord.ext import commands
import os
from decouple import config

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Streaming(name="Minecraft", url="https://www.twitch.tv/frankliang8"))
    print(client.activity)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Check member status
@client.event
async def on_member_update(before, after):
    print(before)
    if before.status != after.status:
        embed = discord.Embed(title=f"Changed status")
        embed.add_field(name='User', value=before.mention)
        embed.add_field(name='Before', value=before.status)
        embed.add_field(name='After', value=after.status)
        print(embed)
        # send to admin or channel you choose
        channel = client.get_channel('827015029609857034')  # notification channel
        await channel.send(embed=embed)
        # admin = client.get_user(827015029609857034)  # admin to notify
        # await admin.send(embed=embed)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client.run(config('TOKEN'))