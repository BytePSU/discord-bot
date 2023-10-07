import discord

#Intents allow the bot to retrieve certain events
intent = discord.Intents.default()
intent.message_content = True

client = discord.client(intent=intent)


bot_name = "BytePSU"

#on_ready() begins when the program runs and outputs a statement letting the user know 
@client.event
async def on_ready():
    print(f"{bot_name} is now running")
