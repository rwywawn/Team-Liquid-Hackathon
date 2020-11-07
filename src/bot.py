import discord
from config import Config
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('https://discord.com/api/oauth2/authorize?client_id=774513868365234226&redirect_uri=http%3A%2F%2Flocalhost%2F&response_type=code&scope=connectionsD')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(Config['token'])