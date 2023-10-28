import os
from datetime import datetime
from random import randint
import traceback

import openai
import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()

from utils import internship as its 
from utils.color import calc_avg_color
its.update_file()


class Bot(discord.Client):  
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        '''CommandTrees hold all the cmd states required to make slashes work.
        Whenever you work with app cmds, the tree is used to store and work with them.''' 
        self.tree = app_commands.CommandTree(self)
        self.internships_data = its.open_file()
        self.testing = os.getenv('TESTING') == '1'
    
    async def setup_hook(self):
        # This copies the global commands over to the guild/server.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


client = Bot()

TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = os.getenv('BOT_GUILD_ID')
MY_GUILD = discord.Object(id=GUILD_ID)
CHANNEL_ID = [os.getenv('CHANNEL_ID') if not client.testing else os.getenv('TESTING_CHANNEL_ID')][0]

openai.api_key = os.getenv('GPT')


def generate_job_summary(internship):
    '''ChatGPT integration to provide brief summaries of companies'''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user", 
                "content": f"Summarize {internship} in 15 words or less WITHOUT restating the company's name. Be engaging!\n\nSummary:"}
        ],
        temperature=1,
        max_tokens=20,
    )
    return response.choices[0].message.content


def create_internship_embed(index: int):
    '''Beautified messages through discord.py embeds. 
    Displays the internship's location, required education, and pay.'''
    internship_data = client.internships_data

    #Error-handling for out-of-range indices
    if index > len(internship_data) - 1 or index < 0:
        index = 0
        embed = discord.Embed(title=f"Internship #{index} does not exist. Please try again with a different ID.", colour=discord.Colour(0xff0000))
        url_view = discord.ui.View()

        return embed, url_view

    #for ChatGPT text completion
    try: 
        job_summary = generate_job_summary(its.check_for_key(internship_data[index], 'company'))
    except Exception as e: 
        job_summary = None

    #Embed styling
    embed = discord.Embed(description=f"{job_summary} | *Apply now!*\n{'<:D10:1165807583655891004> '*9}\n**{its.check_for_key(internship_data[index], 'title')} • {its.check_for_key(internship_data[index], 'season')} {its.check_for_key(internship_data[index],'yr')}**\n\n:earth_americas:   :dollar:",
                          title=f"{its.check_for_key(internship_data[index], 'company')} (#{index})",
                          colour=discord.Colour(int(calc_avg_color(internship_data[index]['icon']).lstrip('#'), 16)),
                          timestamp=datetime.now())  
    
    embed.set_thumbnail(url=its.check_for_key(internship_data[index], 'icon'))
    embed.add_field(name="Location", value=its.check_for_key(internship_data[index], 'loc'))
    embed.set_footer(text = f"New Internship at {its.check_for_key(internship_data[index], 'company')}")

    if (its.check_for_key(internship_data[index], 'educationLevel') != 'Not Available'): 
        embed.add_field(name="Education", value=its.check_for_key(internship_data[index], 'educationLevel'))
    else: 
        embed.add_field(name="Education", value='Any')
    if (its.check_for_key(internship_data[index], 'hourlySalary') != 'Not Available'): 
        embed.add_field(name="Salary", value=f"${round(its.check_for_key(internship_data[index],'monthlySalary'))}/mo • ${round(its.check_for_key(internship_data[index],'hourlySalary'))}/hr")
    else:
        embed.add_field(name="Salary", value='Unknown')
    
    #Button integration
    url_view = discord.ui.View() 
    url_view.add_item(discord.ui.Button(label='Apply', style=discord.ButtonStyle.url, url=its.check_for_key(internship_data[index], 'link')))
    url_view.add_item(discord.ui.Button(label='Rating', style=discord.ButtonStyle.green))

    return embed, url_view


@client.event
async def on_ready():
    print(f'{client.user} is online and running! ({datetime.now()}) ({["Testing" if client.testing else "Normal"]})')
    print('-------------------')
    update.start()


@client.event
async def update_account_status(internship_amount: int):
    '''Changes the status of the bot in real time.'''
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{internship_amount} internship{'s' if internship_amount > 1 else ''}"))
    print(f"Bot status changed to Watching", f"{internship_amount} internship{'s' if internship_amount > 1 else ''}")


@client.tree.command(name="internship")
async def get_internship(interact: discord.Interaction, index: int):
    '''Outputs an internship at a given index.'''
    print(interact.user, f"asked for internship #{index} on {datetime.now()}")
    try:
        embed, url_view = create_internship_embed(index)
        ping = '<@&1165743852708180049>' #to notify interested users

        await interact.response.send_message(ping, embed=embed, view=url_view)
    except Exception as e:
        await interact.response.send_message(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        return
    

@client.tree.command(name="random_internship")
async def random_internship(interact: discord.Interaction):
    '''Allows user to ask for a random internship.'''
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
    '''Checks for new internships every fifteen minutes. When new internships are 
    detected, they are posted on a Discord channel.'''
    print(f"Initiating a new update on {datetime.now()}")

    channel_to_post = client.get_channel(CHANNEL_ID)
    
    try:
        changes = its.check_for_update()

        if changes["changed"]:
            print("A new update has been detected.")

            its.update_file() 
            client.internships_data = its.open_file() #updates and retrieves new data

            if changes["amount"] > 0:
                print(f"{changes['amount']} new internships found.")

                await channel_to_post.send(f"Update! {changes['amount']} new internship{'s' if changes['amount'] > 1 else ''} has been added! {changes['old_amount']} -> {len(client.internships_data)}")

                if changes["amount"] <= 10:
                    for post in range(len(client.internships_data) - changes["amount"], len(client.internships_data)):
                        embed, url_view = create_internship_embed(post)
                        await channel_to_post.send(embed=embed, view=url_view, silent=True)

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

