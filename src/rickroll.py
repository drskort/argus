from random import random

from discord import VoiceClient, FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get


class Rickroller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def secret(self, ctx, channelName):
        channels = ctx.author.guild.channels
        for ch in channels:
            if ch.name == channelName:
                vc = await ch.connect()
                source = FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source='rickroll.mp4')
                vc.play(source)
