import discord
from Packages import Botloader
import asyncio
import os
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from gtts import gTTS
from random import randint
from typing import List
from Packages.automod import AutoMod

class Common(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cmd_autocompletion(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        cmds = ['play', 'join', 'leave', 'stop', 'vtts', 'ftts', 'dm', 'execute']
        return [
            app_commands.Choice(name=cmd, value=cmd)
            for cmd in cmds if current.lower() in cmd.lower()
        ]
    
    async def lg_autocompletion(self, interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
            lgs = ['fr','ja','de','en']
            return [
                    app_commands.Choice(name=lg, value=lg)
                    for lg in lgs if current.lower() in lg.lower()
                ]

    @commands.hybrid_command(name="bugreport", help = f"Signaler un bug.")
    @app_commands.autocomplete(command = cmd_autocompletion)
    async def bugreport(self, ctx: Context, command, bug: str):
        guild = self.bot.get_guild(Botloader.Bot.BotGuild)
        channel = guild.get_channel_or_thread(Botloader.Bot.BugReportChannel)
        embed = discord.Embed(title="Rapport de Bug", description=f"Commande concernée `{command}`.", colour=discord.colour.Color.orange())
        embed.add_field(name="Bug:", value=bug, inline=False)
        embed.add_field(name="Etat de correction:", value="En cour...", inline=False)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
        view = discord.ui.View()
        item = discord.ui.Button(style=discord.ButtonStyle.green, label="Corriger", custom_id="bugreport_correction", disabled=False)
        view.add_item(item=item)
        item = discord.ui.Button(style=discord.ButtonStyle.grey, label="Non Recevable", custom_id="bugreport_correction_n", disabled=False)
        view.add_item(item=item)
        await channel.send(embed=embed, view=view)
        await ctx.reply("Merci d'avoire signalé le bug! \n Si vous avez des question contactez nous: <support@gamebot.smaugue.lol>", ephemeral=True)
        
    @commands.hybrid_command(name="sayic", help = f"Permet de fair parler le bot dans un channel définit.")
    @commands.guild_only()
    async def sayInChannel(self, ctx: Context, channel : discord.TextChannel, text):
        blw, blws = AutoMod.check_message(text)
        if len(blw) != 0:
            return await ctx.reply("Veuillez surveiller votre langage.")
        if Botloader.Data.get_user_conf(ctx.guild.id, ctx.author.id, Botloader.Data.cmd_value['sayic']) != "1":
            return await Botloader.Bot.on_refus_interaction(ctx)
        await channel.send(text)
        await ctx.reply(f"Votre message a bien été envoyé dans #{channel}!")

    @commands.hybrid_command(name="say", help = f"Permet de fair parler le bot.")
    @commands.guild_only()
    async def say(self, ctx: Context, text):
        blw, blws = AutoMod.check_message(text)
        if len(blw) != 0:
            return await ctx.reply("Veuillez surveiller votre langage.")
        if Botloader.Data.get_user_conf(ctx.guild.id, ctx.author.id, Botloader.Data.cmd_value['say']) == "0":
            return await Botloader.Bot.on_refus_interaction(ctx)
        await ctx.send(text)

    @commands.hybrid_command(name="vtts")
    @app_commands.autocomplete(lg = lg_autocompletion)
    @commands.guild_only()
    async def vtts(self, ctx: Context, lg, *, text_to_speak: str):
        blw, blws = AutoMod.check_message(text_to_speak)
        if len(blw) != 0:
            return await ctx.reply("Veuillez surveiller votre langage.")
        if Botloader.Data.get_user_conf(ctx.guild.id, ctx.author.id, Botloader.Data.cmd_value['vtts']) == "0":
            return await Botloader.Bot.on_refus_interaction(ctx)
        if ctx.voice_client is None:
            await ctx.send("Le bot n'est pas connecté à un canal vocal. Utilisez !join pour le faire rejoindre un canal vocal.", ephemeral=True)
            return
        await ctx.defer()
        try:
            tts = gTTS(text=text_to_speak, lang=lg)
            tts.save('output.mp3')
            await Botloader.Bot.play_audio(ctx,'output.mp3')
            await ctx.reply('Succès.', ephemeral=True)
        except Exception as e:
            await ctx.reply(f"Une erreur est survenue: {e} \n N'ésitez pas à faire un `/bugreport`")
        
    @commands.hybrid_command(name="ftts")
    @app_commands.autocomplete(lg = lg_autocompletion)
    @commands.guild_only()
    async def ftts(self, ctx: Context, lg, text_to_speak: str):
        blw, blws = AutoMod.check_message(text_to_speak)
        if len(blw) != 0:
            return await ctx.reply("Veuillez surveiller votre langage.")
        if Botloader.Data.get_user_conf(ctx.guild.id, ctx.author.id, Botloader.Data.cmd_value['ftts']) == "0":
            return await Botloader.Bot.on_refus_interaction(ctx)
        try:
            tts = gTTS(text=text_to_speak, lang=lg)
        except:
            return await ctx.reply("Nous ne parvenons pas à générer la naration.")
        tts.save('output.mp3')
        try:
            async with ctx.typing():
                with open('output.mp3', 'rb') as f:
                    await ctx.send(file=discord.File(f, filename='output.mp3'))
        finally:
            os.remove('output.mp3')

        
    @commands.hybrid_command(name = "rdm")
    @commands.guild_only()
    async def randome(self, ctx: Context, min: int, max: int):
        if Botloader.Data.get_user_conf(ctx.guild.id, ctx.author.id, Botloader.Data.cmd_value['rdm']) == "0":
            return await Botloader.Bot.on_refus_interaction(ctx)
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