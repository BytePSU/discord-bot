
import discord
import responses
import os


#Intents allow the bot to retrieve certain events
intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)

key = os.environ.get("DISCORD_TOKEN")
bot_name = "BytePSU"

#on_ready() begins when the program runs and outputs a statement letting the user know 
@client.event
async def on_ready():
    print(f"{bot_name} is now running")

@client.event
async def on_message(message):
    prompt = message
    if message.author == client.user:
        return
    if message.content.startswith('/we are'):
        await message.channel.send('We are PENN STATE!')
    elif message.content.startswith('/hello'):
        await message.channel.send('Whats up!')
    else:
        await message.channel.send('I dont know what you said')

client.run(key)


