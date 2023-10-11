import discord
from discord import app_commands
import random
import os
from dotenv import load_dotenv, find_dotenv
import json
import requests


load_dotenv()
# Intents allow the bot to retrieve certain events
intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)
tree = app_commands.CommandTree(client)

key = os.getenv('BOT_TOKEN')
guild_id = os.getenv('BOT_GUILD_ID')
bot_name = 'BytePSU'


def check_for_key(internship, key):
    try:
        return internship[key] if internship[key] != "" else "None"
    except:
        if key == "link":
            return "https://www.levels.fyi/js/internshipData.json"
        elif key == "icon":
            return "https://cdn.discordapp.com/embed/avatars/0.png"
        return 'Unknown'


with open('./database/internships.json') as f:
    internships_data = json.load(f)

# Now you can use the `data` variable to access the contents of the JSON file

# on_ready() begins when the program runs. It syncs the tree when called, and outputs a statement letting the user know the bot is ready.


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print(f"{bot_name} is now running")


@tree.command(name="we_are", description="Responds with the Penn State chant.", guild=discord.Object(id=guild_id))
async def we_are(interact):
    await interact.response.send_message('We are PENN STATE!')


@tree.command(name="hello", description="Responds with a greeting message.", guild=discord.Object(id=guild_id))
async def hello(interact):
    await interact.response.send_message('Whats up!')


@tree.command(name="get_internship", description="Grabs internship data of given index.", guild=discord.Object(id=guild_id))
async def get_internship(interact, index: int):
    with open('utils/embed_colors.txt', 'r') as f:
        random_colors = [int(line.strip(), 16) for line in f.readlines()]
        color = random.choice(random_colors)

    if index > len(internships_data) or index < 0:
        await interact.response.send_message(f"Internship #{index} does not exist.")
        return

    embed = discord.Embed(title=f"Internship #{index}",
                          colour=discord.Colour(color),
                          url=check_for_key(internships_data[index], 'link'))

    embed.set_thumbnail(url=check_for_key(internships_data[index], 'icon'))
    embed.set_footer(
        text="BytePSU", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="Company", value=check_for_key(
        internships_data[index], 'company'))
    embed.add_field(name="Job Title", value=check_for_key(
        internships_data[index], 'title'))
    embed.add_field(name="Required Education", value=check_for_key(
        internships_data[index], 'educationLevel'))
    embed.add_field(
        name="Year", value=f"{check_for_key(internships_data[index],'season')} {check_for_key(internships_data[index],'yr')}")
    embed.add_field(name="Location", value=check_for_key(
        internships_data[index], 'loc'))
    embed.add_field(
        name="Salary", value=f"${check_for_key(internships_data[index],'monthlySalary')}/mo\n${check_for_key(internships_data[index],'hourlySalary')}/hr")
    
    embed.add_field(name="More Details", value=check_for_key(
        internships_data[index], 'moreInfo'))

    await interact.response.send_message(embed=embed)


client.run(key)
