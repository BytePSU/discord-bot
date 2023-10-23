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
    #await client.get_channel(1160282313859530854).send(f'{client.user} is online and running! - {datetime.now()}')
    print(f'{client.user} is online and running! ({datetime.now()})')
    print('-------------------')

    update.start()


async def update_account_status(internship_amount: int):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{internship_amount} internship{'s' if internship_amount > 1 else ''}"))
    print(f"Bot status changed to Watching", f"{internship_amount} internship{'s' if internship_amount > 1 else ''}")

def create_internship_embed(index: int):
    print(f"A new internship embed is being created on {datetime.now()}")

    if index > len(client.internships_data) - 1 or index < 0:
        embed = discord.Embed(title=f"Internship #{index} does not exist. Please try again with a different ID.", colour=discord.Colour(0xff0000))
        url_view = discord.ui.View()
        print("Internship did not exist.")
        return embed, url_view

    print(client.internships_data[index])

    embed = discord.Embed(description=f"<@&1165743852708180049> | Apply now!\n{'<:D10:1165807583655891004>'*17}\n**{its.check_for_key(client.internships_data[index], 'title')} • {its.check_for_key(client.internships_data[index],'yr')}**\n*__Info:__*",
                          title=f"{its.check_for_key(client.internships_data[index], 'company')} (#{index})",
                          colour=discord.Colour(int(calc_avg_color(client.internships_data[index]['icon']).lstrip('#'), 16)))  

    embed.set_thumbnail(url=its.check_for_key(client.internships_data[index], 'icon'))
    embed.add_field(name="Location", value=its.check_for_key(client.internships_data[index], 'loc'))

    if (its.check_for_key(client.internships_data[index], 'educationLevel') != 'Not Available'): 
        embed.add_field(name="Education", value=its.check_for_key(client.internships_data[index], 'educationLevel'))
    else: 
        embed.add_field(name="Education", value='Any')
    if (its.check_for_key(client.internships_data[index], 'hourlySalary') != 'Not Available'): 
        embed.add_field(name="Salary", value=f"${round(its.check_for_key(client.internships_data[index],'monthlySalary'))}/mo • ${round(its.check_for_key(client.internships_data[index],'hourlySalary'))}/hr")
    else:
        embed.add_field(name="Salary", value='Unknown')
    
    url_view = discord.ui.View() 
    url_view.add_item(discord.ui.Button(label='Apply', style=discord.ButtonStyle.url, url=its.check_for_key(client.internships_data[index], 'link')))

    return embed, url_view

@client.tree.command(name="internship")
async def get_internship(interact: discord.Interaction, index: int):
    print(interact.user, f"asked for internship #{index} on {datetime.now()}")
    try:
        embed, url_view = create_internship_embed(index)
        
        await interact.response.send_message(embed=embed, view=url_view)
    except Exception as e:
        await interact.response.send_message(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        return

@client.tree.command(name="random_internship")
async def random_internship(interact: discord.Interaction):
    print(interact.user, f"asked for a random internship on {datetime.now()}")
    try:
        random_index = randint(0, len(client.internships_data) - 1)
        embed, url_view = create_internship_embed(random_index)
        
        await interact.response.send_message(embed=embed, view=url_view)
    except Exception as e:
        await interact.response.send_message(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        return
    

@tasks.loop(minutes=15)
async def update():
    print(f"Initiating a new update on {datetime.now()}")

    channel_to_post = client.get_channel(1160282313859530854)
    
    try:
        changes = its.check_for_update()

        if changes["changed"]:
            print("A new update has been detected.")

            its.update_file()
            client.internships_data = its.open_file()

            if changes["amount"] > 0:
                print(f"{changes['amount']} new internships found.")

                await channel_to_post.send(f"Update! {changes['amount']} new internship{'s' if changes['amount'] > 1 else ''} has been added! {changes['old_amount']} -> {len(client.internships_data)}")

                if changes["amount"] <= 10:
                    for post in range(len(client.internships_data) - changes["amount"], len(client.internships_data)):
                        embed1, embed2, url_view = create_internship_embed(post)
                        await channel_to_post.send(embeds=[embed1, embed2], view=url_view, silent=True)

            elif changes["amount"] < 0:
                print(f'{changes["amount"]} internships have been removed.')
                await channel_to_post.send(f"Update! {changes['amount']} internship{'s' if changes['amount'] > 1 else ''} has been removed! {changes['old_amount']} -> {len(client.internships_data)}")

            await channel_to_post.send(f'\n\nDatabase updated! ({datetime.now()})')
        else:
            print('No new update.')
            print(f"Database is up to date! ({len(client.internships_data)} internships as of {datetime.now()})")


    except Exception as e:
        print(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        await channel_to_post.send(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```", silent=True)
        return
    
    await update_account_status(len(client.internships_data))
    
@client.tree.command(name="test")
async def test_refresh_json(interact: discord.Interaction):
    print("Refreshing json")
    client.internships_data = its.open_file()
    await interact.response.send_message(f"json file refreshed, {len(client.internships_data)}")
    



client.run(TOKEN)
