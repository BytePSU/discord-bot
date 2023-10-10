import discord
from discord import app_commands
import random 
import os



#Intents allow the bot to retrieve certain events
intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)
tree = app_commands.CommandTree(client)

key = os.environ.get("DISCORD_TOKEN")
guild_id = os.environ.get("DISCORD_GUILD_ID")
bot_name = "BytePSU"


# on_ready() begins when the program runs. It syncs the tree when called, and outputs a statement letting the user know the bot is ready.
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print(f"{bot_name} is now running")

@tree.command(name = "we_are", description = "Responds with the Penn State chant.", guild=discord.Object(id=guild_id))
async def we_are(interact):
    await interact.response.send_message('We are PENN STATE!')

@tree.command(name = "hello", description = "Responds with a greeting message.", guild=discord.Object(id=guild_id))
async def hello(interact):
    await interact.response.send_message('Whats up!')

@tree.command(name = "internship_update", description = "posts internships regularly", guild=discord.Object(id=guild_id))
async def internship_embed(interact): 
    """Embeds internship content with a random color on each post"""
    with open('utils/embed_colors.txt', 'r') as f: 
        random_colors = [int(line.strip(), 16) for line in f.readlines()]
        color = random.choice(random_colors)

    embed = discord.Embed(title="Internship Update", 
                          colour=discord.Colour(color), 
                          url="https://www.levels.fyi/js/internshipData.json")
    

    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="TBD", value="sample text")
    embed.add_field(name="TBD", value="sample text")
    embed.add_field(name="TBD", value="sample text")
    embed.add_field(name="TBD-inline", value="test-1", inline=True)
    embed.add_field(name="TBD-inline", value="test-2", inline=True)

    await interact.response.send_message(embed=embed)


client.run(key)