# client.py
import os
import discord

from discord.ext import commands

from dotenv import load_dotenv

from greeter import Greeter
from reactionroles import ReactionRoles
from roll.roll import Roll
from rickroll import Rickroller

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

description = '''The watcher that oversees the Spire.'''

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.add_cog(Greeter(bot))
    await bot.add_cog(Rickroller(bot))
    await bot.add_cog(Roll(bot))
    await bot.add_cog(ReactionRoles(bot))

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"I am sorry {ctx.author.name}, but I didn't understand your command. \n"
                   f"\"{str(error)}\"")
    print(str(error))

bot.run(TOKEN)
