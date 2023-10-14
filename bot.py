import os
from datetime import datetime
import json

import discord
from discord import app_commands
from dotenv import load_dotenv

from utils import internship as its 
from utils.color import calc_avg_color



its.update()
load_dotenv()


TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = os.getenv('BOT_GUILD_ID')
MY_GUILD = discord.Object(id=GUILD_ID)


with open('database/internships.json', 'r') as f:
    internships_data = json.load(f)
    f.close()



class Bot(discord.Client):  
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        '''CommandTrees hold all the cmd states required to make slashes work.
        Whenever you work with app cmds, the tree is used to store and work with them.''' 
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        # This copies the global commands over to the guild/server.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)



client = Bot()

@client.event
async def on_ready():
    print(f'{client.user} is online and running! ({datetime.now()})')
    print('------')


@client.tree.command(name="internship")
async def get_internship(interact, index: int):

    if index > len(internships_data) or index < 0:
        await interact.response.send_message(f"Internship #{index} does not exist. Try again.")
        return

    embed = discord.Embed(title=f"Internship #{index}",
                          colour=discord.Colour(int(calc_avg_color(internships_data[index]['icon']).lstrip('#'), 16)),
                          url=its.check_for_key(internships_data[index], 'link'))

    embed.set_thumbnail(url=its.check_for_key(internships_data[index], 'icon'))
    embed.add_field(name="Company", value=its.check_for_key(internships_data[index], 'company'))
    embed.add_field(name="Job Title", value=its.check_for_key(internships_data[index], 'title'))
    embed.add_field(name="Required Education", value=its.check_for_key(internships_data[index], 'educationLevel'))
    embed.add_field(name="Year", value=f"{its.check_for_key(internships_data[index],'season')} {its.check_for_key(internships_data[index],'yr')}")
    embed.add_field(name="Location", value=its.check_for_key(internships_data[index], 'loc'))
    embed.add_field(name="Salary", value=f"${its.check_for_key(internships_data[index],'monthlySalary'):.2f}/mo\n${its.check_for_key(internships_data[index],'hourlySalary'):.2f}/hr")
    
    url_view = discord.ui.View() 
    url_view.add_item(discord.ui.Button(label='Apply', style=discord.ButtonStyle.url, url=its.check_for_key(internships_data[index], 'link')))
    url_view.add_item(discord.ui.Button(label='Test', style=discord.ButtonStyle.green))
    await interact.response.send_message(embed=embed, view=url_view)



client.run(TOKEN)
