import discord
from discord.ext import commands
from discord.ext.commands import Context
import Botloader
import asyncio
import os
from gtts import gTTS
from random import randint

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot