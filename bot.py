import os
from datetime import datetime
import traceback

import json
import discord
from discord import app_commands
from dotenv import load_dotenv

from utils import internship as its 
from utils.color import calc_avg_color


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = os.getenv('BOT_GUILD_ID')
MY_GUILD = discord.Object(id=GUILD_ID)


#its.update_file()


class Bot(discord.Client):  
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        '''CommandTrees hold all the cmd states required to make slashes work.
        Whenever you work with app cmds, the tree is used to store and work with them.''' 
        self.tree = app_commands.CommandTree(self)
        self.internships_data = its.open_file()
    
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
    try:
        if index > len(client.internships_data) or index < 0:
            await interact.response.send_message(f"Internship #{index} does not exist. Try again.")
            return

        embed = discord.Embed(title=f"Internship #{index} - {its.check_for_key(client.internships_data[index], 'company')}",
                            colour=discord.Colour(int(calc_avg_color(client.internships_data[index]['icon']).lstrip('#'), 16)),
                            url=its.check_for_key(client.internships_data[index], 'link'))
                            

        embed.set_thumbnail(url=its.check_for_key(client.internships_data[index], 'icon'))
        embed.add_field(name="Company", value=its.check_for_key(client.internships_data[index], 'company'))
        embed.add_field(name="Job Title", value=its.check_for_key(client.internships_data[index], 'title'))
        embed.add_field(name="Required Education", value=its.check_for_key(client.internships_data[index], 'educationLevel'))
        embed.add_field(name="Year", value=f"{its.check_for_key(client.internships_data[index],'season')} {its.check_for_key(client.internships_data[index],'yr')}")
        embed.add_field(name="Location", value=its.check_for_key(client.internships_data[index], 'loc'))
        embed.add_field(name="Salary", value=f"${its.check_for_key(client.internships_data[index],'monthlySalary')}/mo\n${its.check_for_key(client.internships_data[index],'hourlySalary')}/hr")
        
        url_view = discord.ui.View() 
        url_view.add_item(discord.ui.Button(label='Apply', style=discord.ButtonStyle.url, url=its.check_for_key(client.internships_data[index], 'link')))
        url_view.add_item(discord.ui.Button(label='Test', style=discord.ButtonStyle.green))
        await interact.response.send_message(embed=embed, view=url_view)
    except Exception as e:
        await interact.response.send_message(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        return
    

@client.tree.command(name="update")
async def update(interact):
    try:
        message = ""
        changes = its.check_for_update()

        if changes["changed"]:
            its.update_file()
            client.internships_data = its.open_file()

            if changes["amount"] > 0:
                message += f"Update! {changes['amount']} new internships have been added!"
            elif changes["amount"] < 0:
                message += f"Update! {changes['amount']} internships have been removed!"

            message += f'\n\nDatabase updated! ({changes["old_amount"]} -> {len(client.internships_data)})'
        
            await interact.response.send_message(message)
        else:
            await interact.response.send_message(f"Database is up to date! ({len(client.internships_data)} internships)")

    except Exception as e:
        await interact.response.send_message(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        return
    
@client.tree.command(name="test")
async def test(interact):
    client.internships_data = its.open_file()

    await interact.response.send_message(f"json file refreshed, {len(client.internships_data)}")



client.run(TOKEN)
