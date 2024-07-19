import discord
import Packs.Botloader
import asyncio
import os
from discord.ext import commands
from discord.ext.commands import Context
from gtts import gTTS
from random import randint

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot