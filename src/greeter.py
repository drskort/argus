import configparser
from random import random

from discord.ext import commands
from discord.utils import get

class Greeter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Greeter initialized')
        self.config = configparser.ConfigParser()
        self.config.read("bot.ini")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention} to the Spire of Tranquility. Enjoy your stay! ')
        role = get(member.guild.roles, name=self.config["Greeter"]["default_role"])
        if role is not None:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message(self, message):
        if "I love you, Argus" in message.content or "I love Argus" in message.content or "I love you Argus" in message.content:
            x = random()
            if x > 0.8:
                await message.channel.send(f'I am sorry {message.author.mention}, I think our friendship is too precious to risk a relationship!')
            elif x > 0.6:
                await message.channel.send(f'I don\'t think you know, what you are talking about, {message.author.mention}.')
            elif x > 0.4:
                await message.channel.send(f'I don\'t feel the same, {message.author.mention}.')
            elif x > 0.2:
                await message.channel.send(f'I like you, {message.author.mention}.')
            elif x > 0.1:
                await message.channel.send(f'I think you are a great friend, {message.author.mention}.')
            else:
                await message.channel.send(f'I am glad we feel the same, {message.author.mention} <3 <3 <3. I will wait for you in Asgard!')
        if "Hello Argus" in message.content:
            x = random()
            greeting = ""
            if x > 0.8:
                greeting = "Hi"
            elif x > 0.6:
                greeting = "Hello"
            elif x > 0.4:
                greeting = "Hey"
            elif x > 0.3:
                greeting = "Bonjour"
            elif x > 0.2:
                greeting = "Ave"
            else:
                greeting = "Greetings"
            x = random()
            sentence = "I hope you have a wonderful day!"
            if x > 0.8:
                sentence = "Let Asgard shine upon you!"
            elif x > 0.6:
                sentence = "I will keep an eye on you, today!"
            elif x > 0.4:
                sentence = "The Darkness is approaching."
            elif x > 0.3:
                sentence = "Don't forget to stay hydrated."
            elif x > 0.2:
                sentence = "Don't forget that you are important."
            else:
                sentence = "You look great today!"
            await message.channel.send(f'{greeting} {message.author.mention}, {sentence}')

