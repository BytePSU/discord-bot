import discord
from discord import app_commands
import random 
import os
from dotenv import load_dotenv, find_dotenv
import json

def check_for_key(internship, key):
    try:
        return internship[key] if internship[key] != "" else "None"
    except:
        if key == "link":
            return "https://www.levels.fyi/js/internshipData.json"
        elif key == "icon":
            return "https://cdn.discordapp.com/embed/avatars/0.png"
        return 'Unknown'

load_dotenv()

#Intents allow the bot to retrieve certain events
intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)
tree = app_commands.CommandTree(client)

key = os.getenv('BOT_TOKEN')
guild_id = os.getenv('BOT_GUILD_ID')
bot_name = 'BytePSU'

levelsfyi_link = "https://www.levels.fyi/js/internshipData.json"
levelsfyi_json = requests.get(levelsfyi_link).text
internships = json.loads(levelsfyi_json)

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

@tree.command(name = "get_internship", description="Grabs internship data of given index.", guild=discord.Object(id=guild_id))
async def get_internship(interact, index: int):
    if index > len(internships) or index < 0:
        await interact.response.send_message(f"Internship #{index} does not exist.")
        return

    embed = discord.Embed(title=f"Internship #{index}", 
                          colour=discord.Colour(0x97b9fa), 
                          url=check_for_key(internships[index],'link'))
    
    embed.set_thumbnail(url=check_for_key(internships[index],'icon'))
    embed.set_footer(text="BytePSU", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="Hiring Company", value=check_for_key(internships[index],'company'))
    embed.add_field(name="Job Title", value=check_for_key(internships[index],'title'))
    embed.add_field(name="Required Education", value=check_for_key(internships[index],'educationLevel'))
    embed.add_field(name="Year", value=f"{check_for_key(internships[index],'season')} {check_for_key(internships[index],'yr')}")
    embed.add_field(name="Location", value=check_for_key(internships[index],'loc'))
    embed.add_field(name="Salary", value=f"${check_for_key(internships[index],'monthlySalary')} / month\n(${check_for_key(internships[index],'hourlySalary')} / hr)")
    embed.add_field(name="More Details", value=check_for_key(internships[index],'moreInfo'))

    await interact.response.send_message(embed=embed)

client.run(key)