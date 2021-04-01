import discord
import os
from decouple import config

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client.run(config('TOKEN'))