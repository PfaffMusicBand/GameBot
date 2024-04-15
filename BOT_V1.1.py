import discord
import asyncio
import os
from random import randint
from typing import Any
from discord import app_commands
from discord.ext import tasks, commands
from datetime import datetime
from gtts import gTTS
import ffmpeg
import random
import Botloader 
import requests
 
intents = discord.Intents.default()
intents.message_content = True
r = "n"
bot = client = commands.Bot(command_prefix = "?",intents=discord.Intents.all(),description = "GameHub France")
bot.remove_command('help')

statutpresence = ["streem in GameHub", "GameHub"]

@bot.event
async def on_ready():
    startTime = datetime.strftime(datetime.now(), '%H:%M:%S')
    print(f'{startTime}|[START/info](/)|Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(status = discord.Status.online,activity = discord.Game("Chargement des cookis!"))
    try:
        synced = await bot.tree.sync()
        print(f'{startTime}|[START/info](/)|Synced {len(synced)} commands')
    except Exception as e:
        print(f"{startTime}|[START/failure](X)|an error has occurred:{e}")
    statut = randint(0,1)
    if statut == 1:
        actype = discord.ActivityType.playing
    else : actype = discord.ActivityType.watching
    statut = statutpresence[statut]
    await bot.change_presence(activity=discord.Activity(type = actype, name = statut))
    print("")

@bot.command()
@commands.has_permissions(administrator=True)
async def restart(ctx,):
    startTime = datetime.strftime(datetime.now(), '%H:%M:%S')
    await ctx.send("Bot was offline for restart.")
    await asyncio.sleep(3)
    print("")
    print(f"{startTime}|[STOP/info](/)|Bot Closed for restart")
    print("")
    global r
    r = "y"
    await bot.close()


@bot.tree.command(name = "gamehubsay")
@app_commands.describe(arg = "Bot say")
async def slashsay(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"{arg}")


@bot.command()
async def say(ctx,*, text):
    messagetodelete = ctx.message
    await messagetodelete.delete()
    await ctx.send(text)
    channel= ctx.channel

#randome générator
@bot.command()
async def rdm(ctx, min,*, max):
    if int(max) > int(min):
        num = randint(int(min), int(max))
    else: num = randint(int(max), int(min))
    embed = discord.Embed(title = "Random", description = f"Voici un nombre aléatoir entre {min} et {max}")
    embed.set_thumbnail(url = "https://media.tenor.com/IfbgWLbg_88AAAAC/dice.gif")
    embed.add_field(name="Nombre:", value= num, inline= False)
    await ctx.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 1141683944077672519:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        if payload.emoji.name == '🍉':
            role = guild.get_role(1124030728271831160)
            reaction_emoji = '🍉'
        if payload.emoji.name == ':pineapple:':
            role = guild.get_role(1124031814500110417)
            reaction_emoji = ':pineapple:'
        if payload.emoji.name == '🍆':
            role = guild.get_role(1124031110058352761)
            reaction_emoji = '🍆'
        if payload.emoji.name == ':peach:':
            role = guild.get_role(1124031374928650291)
            reaction_emoji = ':peach:'
        if role is not None:
            member = guild.get_member(payload.user_id)
            if member is not None:
                reaction_limit = 3
                channel = bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(message_id)
                reaction_count = 0
                for reaction in message.reactions:
                    if str(reaction.emoji) == reaction_emoji:
                        reaction_count = reaction.count
                        break
                if reaction_count <= reaction_limit:
                    await member.add_roles(role)
                    print("Role added to member")
                else:
                    print("Reaction limit reached")
            else:
                print("Member not found")
        else:
            print("Role not found")

@bot.command()
async def join(ctx):
    if ctx.voice_client is not None:
        await ctx.send("Le bot est déjà connecté à un canal vocal.")
        return
    if ctx.author.voice is None:
        await ctx.send("Vous devez être dans un canal vocal pour utiliser cette commande.")
        return
    await ctx.author.voice.channel.connect()

@client.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client.is_recording():
        return
    await ctx.send(f'Stopping the Recording')

    wav_bytes = await ctx.voice_client.stop_record()

    name = str(random.randint(000000, 999999))
    with open(f'{name}.wav', 'wb') as f:
        f.write(wav_bytes)
    await ctx.voice_client.disconnect()


blackliste = [831971146386636820,388026287941484544,852926734860943403] #533699465706471467

@bot.tree.command(name = "vtts")
async def slashsay(interaction: discord.Interaction, tts: str):
    if interaction.user.id not in blackliste:
        for voice_client in client.voice_clients:
            if  voice_client.connect(reconnect=False, timeout=None):
                ibc = True
                break
        if ibc:
            tts = gTTS(text=tts, lang="fr")
            tts.save('output.mp3')
            ibc = False
            ffmpeg_options = {
            'options': '-filter:a "volume= 2.0"'
            }
            voice_client.play(discord.FFmpegPCMAudio('output.mp3', executable=Botloader.FFMPEG.executable, **ffmpeg_options))
            await interaction.response.send_message("Succès", ephemeral=True)
            while voice_client.is_playing():
                await asyncio.sleep(1)
            os.remove('output.mp3')
        else:
            await interaction.response.send_message("Le bot n'est pas connecté ton canal vocal. Utilisez ?join pour le lui faire rejoindre.", ephemeral=True)
    else: await interaction.response.send_message("Nop!", ephemeral=True)

@bot.command()
async def tts(ctx, lg, *, text_to_speak):
    if ctx.author.id not in blackliste:
        tts = gTTS(text=text_to_speak, lang=lg)
        tts.save('output.mp3')
        if ctx.voice_client is None:
            await ctx.send("Le bot n'est pas connecté ton canal vocal. Utilisez ?join pour le lui faire rejoindre.")
            return
        volume_factor = 2.0
        ffmpeg_options = {
            'options': f'-filter:a "volume={volume_factor}"'
        }
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable=Botloader.FFMPEG.executable,source='output.mp3', **ffmpeg_options))
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        os.remove('output.mp3')

@bot.command()
async def play(ctx, *, musique):
    if ctx.voice_client is None:
        await ctx.send("Le bot n'est pas connecté à un canal vocal. Utilisez ?join pour le faire rejoindre un canal vocal.")
        return
    volume_factor = 0.30
    ffmpeg_options = {
        'options': f'-filter:a "volume={volume_factor}"'
    }
    ctx.voice_client.play(discord.FFmpegPCMAudio(executable=ffmpeg,source=f'{musique}.mp3', **ffmpeg_options))
    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)

@bot.command()
async def ftts(ctx,lg, *, text_to_speak):
    tts = gTTS(text=text_to_speak, lang=lg)
    tts.save('output.mp3')
    with open('output.mp3', 'rb') as f:
        await ctx.send(file=discord.File(f, filename='output.mp3'))
    os.remove('output.mp3')

bot.run(Botloader.GameHub.__Token__)
os.system(f"python Launcher.py --bot {Botloader.GameHub.Name} --version 1.1 --restart {r}")