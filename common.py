import discord
from discord.ext import commands
from discord.ext.commands import Context
import Botloader
import asyncio
import os
from gtts import gTTS
from random import randint

class Common(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="sayic", help = f"Permet de fair parler le bot dans un channel définit.")
    async def sayInChannel(self, ctx: Context, channel : discord.TextChannel, text):
        await channel.send(text)
        await ctx.channel.send(f"Votre message a bien été envoyé dans #{channel}!")
        await asyncio.sleep(4)

#\n Syntaxe:`{Botloader.Bot.Prefix}say arg:str`
    @commands.hybrid_command(name="say", help = f"Permet de fair parler le bot.")
    async def say(self, ctx: Context, text):
        await ctx.send(text)
    
    blackliste = [831971146386636820,388026287941484544,852926734860943403,423500858756694016]

    @commands.hybrid_command(name="vtts")
    async def vtts(self, ctx: Context, lg, *, text_to_speak):
        if ctx.voice_client is None:
            await ctx.send("Le bot n'est pas connecté à un canal vocal. Utilisez !join pour le faire rejoindre un canal vocal.", ephemeral=True)
            return
        if ctx.author.id in Common.blackliste:
            return ctx.send("vas te laver")
        tts = gTTS(text=text_to_speak, lang=lg)
        tts.save('output.mp3')
        ctx.voice_client.play(discord.FFmpegPCMAudio(source='output.mp3'))
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        await ctx.reply("Succes", ephemeral=True)
        os.remove('output.mp3')
    
    @commands.command(name="join")
    async def join(self, ctx: Context):
        if ctx.voice_client is not None:
            await ctx.send("Le bot est déjà connecté à un canal vocal.")
            return
        if ctx.author.voice is None:
            await ctx.send("Vous devez être dans un canal vocal pour utiliser cette commande.")
            return
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(name="leave")
    async def leave(self, ctx:Context):
        if ctx.voice_client is None:
            await ctx.send("Le bot n'est pas connecté à un canal vocal.")
            return
        await ctx.voice_client.disconnect()
        
    @commands.hybrid_command(name="ftts")
    async def ftts(self, ctx: Context, lg, text_to_speak):
        try:
            tts = gTTS(text=text_to_speak, lang=lg)
        except:
            await ctx.reply("Nous ne parvenons pas à générer la naration.")
        if commands.MissingRequiredArgument:
            await ctx.reply("Il faut spécifier le texte à narrer.")
            return
        tts.save('output.mp3')
        with open('output.mp3', 'rb') as f:
            await ctx.send(file=discord.File(f, filename='output.mp3'))
        os.remove('output.mp3')
        
    @commands.hybrid_command(name = "rdm")
    async def randome(self, ctx: Context, min: int, max: int):
        try:
            if int(max) > int(min):
                num = randint(int(min), int(max))
            else:
                num = randint(int(max), int(min))
            embed = discord.Embed(title="Random", description=f"Voici un nombre aléatoire entre {min} et {max}")
            embed.set_thumbnail(url="https://media.tenor.com/IfbgWLbg_88AAAAC/dice.gif")
            embed.add_field(name="Nombre:", value=num, inline=False)
            await ctx.reply(embed=embed)
        except Exception as e:
            Botloader.Bot.console("WARN", e)

def setup(bot):
    bot.add_cog(Common(bot))