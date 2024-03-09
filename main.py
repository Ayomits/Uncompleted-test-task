import disnake
from disnake.ext import commands
from config import TOKEN
import os

client = commands.Bot(command_prefix='.', intents=disnake.Intents.all(), case_insensitive=True, reload=True)

@client.event
async def on_ready():
    print(client.user.name)

for root, dirs, files in os.walk('./cogs'):
    for file in files:
          if file.endswith(".py"):
            print(f'Модуль {file[:-3]} загружен')
            client.load_extension(os.path.join(root, file)[2:][:-3].replace(os.path.sep, '.'))

client.run(TOKEN)