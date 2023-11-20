import os
from datetime import datetime
from random import randint
import traceback

import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv
load_dotenv()

from utils import internship as its 
from utils.color import calc_avg_color
from utils.job_descriptions import generate_job_summary
from utils.format_dt import current_time
#its.update_file()


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

def create_internship_embed(index: int, ai: bool = False):
    '''Beautified messages through discord.py embeds. 
    Displays the internship's location, required education, and pay.'''
    internship_data = client.internships_data

    #Error-handling for out-of-range indices
    if index > len(internship_data) - 1 or index < 0:
        embed = discord.Embed(title=f"Internship #{index} does not exist. Please try again with a different ID.", colour=discord.Colour(0xff0000))
        url_view = discord.ui.View()

        return embed, url_view

    #for ChatGPT text completion
    job_summary, more_results_link = generate_job_summary(its.check_for_key(internship_data[index], 'company'), ai)

    #Embed styling
    embed = discord.Embed(description=f"{job_summary}\n**(Summary incorrect? [Click here for more results.]({more_results_link}))**\n{'<:D10:1165807583655891004> '*9}\n**{its.check_for_key(internship_data[index], 'title')} • {its.check_for_key(internship_data[index], 'season')} {its.check_for_key(internship_data[index],'yr')}**",
                          title=f"{its.check_for_key(internship_data[index], 'company')} (#{index})",
                          colour=discord.Colour(int(calc_avg_color(internship_data[index]['icon']).lstrip('#'), 16)),
                          timestamp=datetime.now())  
    


    embed.set_thumbnail(url=its.check_for_key(internship_data[index], 'icon'))


    if (its.check_for_key(internship_data[index], 'loc') != ''):
        embed.add_field(name="Location", value=its.check_for_key(internship_data[index], 'loc'))
    else:
        embed.add_field(name="Location", value='Unknown')
   

    if (its.check_for_key(internship_data[index], 'educationLevel') != ''): 
        embed.add_field(name="Education", value=its.check_for_key(internship_data[index], 'educationLevel'))
    else: 
        embed.add_field(name="Education", value='Unknown')


    if (its.check_for_key(internship_data[index], 'hourlySalary') != ''): 
        embed.add_field(name="Salary", value=f"${round(its.check_for_key(internship_data[index],'monthlySalary'))}/mo • ${round(its.check_for_key(internship_data[index],'hourlySalary'))}/hr")
    else:
        embed.add_field(name="Salary", value='Unknown')

    
    if (its.check_for_key(internship_data[index], 'moreInfo') != ''): 
        embed.add_field(name="More Info", value=its.check_for_key(internship_data[index], 'moreInfo'))

    
    embed.set_footer(text = f"New Internship at {its.check_for_key(internship_data[index], 'company')}")


    url_view = discord.ui.View() 
    if (its.check_for_key(internship_data[index], 'link') != 'Not Available'):
        url_view.add_item(discord.ui.Button(label='Apply now!', style=discord.ButtonStyle.url, url=its.check_for_key(internship_data[index], 'link')))



    return embed, url_view


@client.event
async def on_ready():
    print(f'{client.user} is online and running! ({current_time()}) ({"Testing" if client.testing else "Normal"})')
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
    print(interact.user, f"asked for internship #{index} on {current_time()}")
    try:
        await interact.response.defer()
        embed, url_view = create_internship_embed(index)
        await interact.followup.send(embed=embed, view=url_view)
    except Exception as e:
        await interact.response.send_message(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        return


@client.tree.command(name="random_internship")
async def random_internship(interact: discord.Interaction):
    '''Allows user to ask for a random internship.'''
    print(interact.user, f"asked for a random internship on {current_time()}")
    
    try:
        random_index = randint(0, len(client.internships_data) - 1)
        print(f'Random internship is #{random_index}')
        
        await interact.response.defer()
        embed, url_view = create_internship_embed(random_index)
        await interact.followup.send(embed=embed, view=url_view)
    except Exception as e:
        await interact.response.send_message(f"An exception has occurred. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")


@tasks.loop(seconds=15)
async def update():
    '''Checks for new internships every fifteen minutes. When new internships are 
    detected, they are posted on a Discord channel.'''
    print(f"Initiating a new update on {current_time()}")

    ping = '<@&1165743852708180049>'
    channel_to_post = client.get_channel(int(CHANNEL_ID))
    
    try:
        status, changes = its.check_for_update()

        if status:
            print("A new update has been detected.")
            await channel_to_post.send(f"{ping}\n# New Internship Update!")

            if len(changes["removed"]) > 0:
                print(f"{len(changes['removed'])} internships have been removed.")
                await channel_to_post.send(f"## Removed Internships", silent=True)
                await channel_to_post.send(f"{len(changes['removed'])} internships have been removed.", silent=True)

                if len(changes["removed"]) <= 10:
                    for post in changes["removed"]:
                        embed, url_view = create_internship_embed(post)
                        await channel_to_post.send(embed=embed, view=url_view, silent=True)

            its.update_file() 
            client.internships_data = its.open_file()

            if len(changes["added"]) > 0:
                print(f"{len(changes['added'])} new internships have been added!")
                await channel_to_post.send(f"## New Internships", silent=True)
                await channel_to_post.send(f"{len(changes['added'])} new internships have been added!", silent=True)

                if len(changes["added"]) <= 10:
                    for post in changes["added"]:
                        embed, url_view = create_internship_embed(post)
                        await channel_to_post.send(embed=embed, view=url_view, silent=True)


            if len(changes["cat_added"]) > 0:
                await channel_to_post.send(f"## Internship Category Additions", silent=True)
                for index,categories in changes["cat_added"].items():
                    print(f"A new category was added for Internship #{index + changes['offset']}!")
                    await channel_to_post.send(f"A new category was added for Internship #{index + changes['offset']}!", silent=True)
                    
                    for category in categories:
                        await channel_to_post.send(f"- {category}", silent=True)

                    embed, url_view = create_internship_embed(index + changes['offset'])
                    await channel_to_post.send(embed=embed, view=url_view, silent=True)


            
            if len(changes["cat_removed"]) > 0:
                await channel_to_post.send(f"## Internship Category Removals", silent=True)
                for index,categories in changes["cat_removed"].items():
                    print(f"A category was removed for Internship #{index + changes['offset']}!")
                    await channel_to_post.send(f"A category was removed for Internship #{index + changes['offset']}!", silent=True)
                    
                    for category in categories:
                        await channel_to_post.send(f"- {category}")

                    embed, url_view = create_internship_embed(index + changes['offset'])
                    await channel_to_post.send(embed=embed, view=url_view, silent=True)


            if len(changes["cat_changed"]) > 0:
                await channel_to_post.send(f"## Internship Changes", silent=True)
                for index,categories in changes["cat_changed"].items():
                    print(f"A value in a category was changed for Internship #{index + changes['offset']}!")
                    await channel_to_post.send(f"A value in a category was changed for Internship #{index + changes['offset']}!", silent=True)

                    for category in categories:
                        await channel_to_post.send(f"- {category[0]} ({category[1]} -> {category[2]})", silent=True)


                    embed, url_view = create_internship_embed(index + changes['offset'])
                    await channel_to_post.send(embed=embed, view=url_view, silent=True)


            print(f"Result: {changes['old_amount']} internships -> {len(client.internships_data)}", silent=True)

            if len(client.internships_data) != changes['old_amount']:
                await channel_to_post.send(f"## Internship Amount", silent=True)
                await channel_to_post.send(f"Result: {changes['old_amount']} internships -> {len(client.internships_data)} internships", silent=True)
            await channel_to_post.send(f'**\n\nDatabase updated! ({current_time()})**', silent=True)
        else:
            print('No new update.')
            print(f"Database is up to date! ({len(client.internships_data)} internships as of {current_time()})")


    except Exception as e:
        print(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```")
        await channel_to_post.send(f"An exception has occured. Please refer to the traceback below and blame someone.\n```{traceback.format_exc()}```", silent=True)
        return
    
    await update_account_status(len(client.internships_data))
    

@client.tree.command(name="force_refresh")
async def force_refresh_json(interact: discord.Interaction):
    print("Forcing refresh on json...")
    client.internships_data = its.open_file()
    await interact.response.send_message(f"json file refreshed, {len(client.internships_data)}")


    



client.run(TOKEN)
