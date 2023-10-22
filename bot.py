import os
from datetime import datetime
import traceback
from random import randint

import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

from utils import internship as its 
from utils.color import calc_avg_color


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = os.getenv('BOT_GUILD_ID')
MY_GUILD = discord.Object(id=GUILD_ID)


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

    update.start()


@client.tree.command(name="internship")
async def get_internship(interact, index: int):
    try:
        # if index > len(client.internships_data) - 1 or index < 0:
        #     await interact.response.send_message(f"Internship #{index} does not exist. Try again.")
        #     return

        embed, url_view = create_internship_embed(index)
        
        await interact.response.send_message(embed=embed, view=url_view)
    except Exception as e:
        await interact.response.send_message(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        return
    

def create_internship_embed(index: int):
    if index > len(client.internships_data) - 1 or index < 0:
        embed = discord.Embed(title=f"Internship #{index} does not exist. Please try again with a different ID.", colour=discord.Colour(0xff0000))
        url_view = discord.ui.View()
        return embed, url_view

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

    return embed, url_view

@client.tree.command(name="random_internship")
async def random_internship(interact):
    try:
        random_index = randint(0, len(client.internships_data) - 1)
        embed, url_view = create_internship_embed(random_index)
        
        await interact.response.send_message(embed=embed, view=url_view)
    except Exception as e:
        await interact.response.send_message(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        return
    

@tasks.loop(seconds=900.0)
async def update():
    channel_to_post = client.get_channel(1160282313859530854)
    
    try:
        changes = its.check_for_update()

        if changes["changed"]:
            its.update_file()
            client.internships_data = its.open_file()

            if changes["amount"] > 0:
                await channel_to_post.send(f"Update! {changes['amount']} new internship{'s' if changes['amount'] > 1 else ''} has been added! {changes['old_amount']} -> {len(client.internships_data)}")

                if changes["amount"] <= 10:
                    for post in range(len(client.internships_data) - changes["amount"], len(client.internships_data)):
                        embed, url_view = create_internship_embed(post)
                        await channel_to_post.send(embed=embed, view=url_view, silent=True)

            elif changes["amount"] < 0:
                await channel_to_post.send(f"Update! {changes['amount']} internship{'s' if changes['amount'] > 1 else ''} has been removed! {changes['old_amount']} -> {len(client.internships_data)}")

            await channel_to_post.send(f'\n\nDatabase updated! ({datetime.now()})')
        else:
            await channel_to_post.send(f"Database is up to date! ({len(client.internships_data)} internships as of {datetime.now()})", silent=True)

    except Exception as e:
        await channel_to_post.send(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```", silent=True)
        return
    
@client.tree.command(name="test")
async def test_refresh_json(interact):
    client.internships_data = its.open_file()
    await interact.response.send_message(f"json file refreshed, {len(client.internships_data)}")
    



client.run(TOKEN)
