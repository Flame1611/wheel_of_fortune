import json
import random
from PIL import Image
import os
from dotenv import load_dotenv
from discord import app_commands
import discord
load_dotenv()

# Gets the bot to exist, and uses slash commands to allow for minimal premissions
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Spaces is a list of every value on the wheel of fortune, in order they appear, clockwise
with open("space_content.json","r") as spaces_list:
    spaces = json.load(spaces_list)
wheel_image = Image.open("wheel_of_fortune.png")

# Syncing slash commands
@tree.command(name='sync', description='Owner only', guild=discord.Object(id=1041157122823565343))
async def sync(interaction: discord.Interaction):
    if interaction.user.id == 555457001522724864:
        await tree.sync()
        print('Command tree synced.')
        await interaction.response.send_message('Done!',ephemeral = True)
    else:
        await interaction.response.send_message('You must be the owner to use this command!',ephemeral = True)

# Generates a random index in the list and rotates the wheel image to match the value at the index
@tree.command(name='spin', description='Spins the wheel')
async def spin(interaction: discord.Interaction):
    number_of_spaces = len(spaces)
    space_number = random.randrange(number_of_spaces)
    save_image = wheel_image.rotate((360/number_of_spaces)*space_number)
    save_image.save('spun_wheel.png',format='png')
    await interaction.response.send_message(f'The wheel spun a {spaces[space_number]}!',file = discord.File('spun_wheel.png'), ephemeral = False)

bot.run(TOKEN)

# Cleanup
os.remove('spun_wheel.png')