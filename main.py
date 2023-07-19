from colorama import Fore, Back, Style
from dotenv import load_dotenv
from discord.ext import tasks
from datetime import datetime
from typing import Optional
from classes import client
from pathlib import Path
import configparser
import discord
import random
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

#LOAD CONFIG PARSER
config = configparser.ConfigParser()
configFile = os.path.join(BASE_DIR, 'settings', 'config.ini')
config.read(configFile)
#LOAD CLIENT CONFIG SETTINGS
TOKEN = config.get('SETTINGS', 'TOKEN')
MY_GUILD = discord.Object(id=config.get('SETTINGS', 'MY_GUILD'))
SUPER_ADMIN = config.get('SETTINGS', 'SUPER_ADMIN')
#LOAD DISCORD CONFIG SETTINGS
SYSTEM_MESSAGES_CHANNEL = int(config.get('DISCORD', 'SYSTEM_MESSAGES_CHANNEL'))
CLIENT = config.get('DISCORD', 'CLIENT')


#DECLARATIONS
intents = discord.Intents.all() # Intent Declaration
client = client.MyClient(MyGuild=MY_GUILD, intents=intents) # Client Instance


#CLIENT ONLINE
@client.event # Login | On Ready Status Message
async def on_ready():
    print(f'{Fore.RED + Style.BRIGHT} Logged in as {client.user} (ID: {client.user.id})')
    print('\n')
    print(f' SuperAdmin: {Style.RESET_ALL}{SUPER_ADMIN}')
    changepresence.start()


@client.event # Client View
async def on_message(message):
    global CLIENT


    if isinstance(message.channel, discord.TextChannel):
            if str(message.author) == CLIENT and len(message.embeds) > 0:
                if message.channel.id == SYSTEM_MESSAGES_CHANNEL: #If message is in System Messages Channel
                    print(f'{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {Fore.BLUE}{Style.BRIGHT}SYSTEM     {Style.NORMAL}{Fore.LIGHTBLACK_EX}{message.embeds[0].author.name}{Style.RESET_ALL} {message.embeds[0].description}')
                else:
                    print(f'{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {Fore.BLUE}{Style.BRIGHT}EMBED     {Style.NORMAL}{Fore.MAGENTA}{message.channel.name} {Fore.LIGHTBLACK_EX}{message.embeds[0].author.name}{Style.RESET_ALL}: {message.embeds[0].description}')
            else:
                if message.attachments: #If message contains attachment
                    print(f'{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {Fore.BLUE}{Style.BRIGHT}MESSAGE     {Style.NORMAL}{Fore.MAGENTA}{message.channel.name} {Fore.LIGHTBLACK_EX}{message.author}{Style.RESET_ALL}: {message.content} {message.attachments[0].url}')
                else:
                    print(f'{Fore.LIGHTBLACK_EX}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {Fore.BLUE}{Style.BRIGHT}MESSAGE     {Style.NORMAL}{Fore.MAGENTA}{message.channel.name} {Fore.LIGHTBLACK_EX}{message.author}{Style.RESET_ALL}: {message.content}')
    elif isinstance(message.channel, discord.DMChannel):
        print(f'Direct Response')


@client.tree.command() #Tree Commands
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')
        
        
@tasks.loop(seconds=10.0)  # How often the bot should change status, mine is set on every 40 seconds
async def changepresence():
    game = [
            discord.Game("Some Game"),
            discord.Game("Some Other Game"),
            discord.Game("Another Game"),
            discord.Game("Idk What Game"),
            discord.Activity(type=discord.ActivityType.watching,name="the Ceiling")
        ]
    for x in range(random.randint(1, len(game))):
        activity = game[x]
    await client.change_presence(activity=activity)


if __name__ == '__main__':
    client.run(TOKEN)