import discord
from discord.ext import commands
import json
with open('config.json') as config_file:
    config = json.load(config_file)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["prefix"], intents=intents, help_command=None)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
async def setup_bot():
    print("Loading extensions...")
    try:
        await bot.load_extension('cogs.help')
        await bot.load_extension('cogs.general')
        await bot.load_extension('cogs.admin')
        await bot.load_extension('cogs.utility')
        await bot.load_extension('cogs.economy')
        print("Extensions loaded successfully")
    except Exception as e:
        print(f"Failed to load extensions: {e}")
if __name__ == "__main__":
    discord.utils.setup_logging()  
    bot.setup_hook = setup_bot  
    bot.run(config["token"])