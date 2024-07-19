import discord
import asyncio
import os
import discord.ext
import discord.ext.commands
from Packages import Botloader
import argparse
import pytz
import glob
from random import randint
from typing import Any
from discord.ext import commands
from datetime import datetime
from gtts import gTTS
from discord.ext.commands import Context
from Packages.automod import AutoMod
from Cogs.common import Common
from Cogs.privat import Privat
from Cogs.owner import Owner
from Cogs.admin import Admin
from Cogs.music import Music
from Packages.version import Version, BOT_VERSION
from Packages.interpretor import parse_actions

def main():
    parser = argparse.ArgumentParser(description='Scripte Bot V1.2')
    parser.add_argument('Botname', type=str, default="Bot", help='Nom du bot à lancer')
    parser.add_argument('--pasword', type=str, default="", help="Mot de passe")
    args = parser.parse_args()
    Botloader.Bot.Launched(args.Botname, str(args.pasword))

if __name__ == '__main__':
    main()

statutpresence = ["you!", "cooked you!"]
r = "n"


class BotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_descriptions = {}

    async def on_ready(self):
        await self.add_cog(Privat(self))#, guild=Botloader.BetaBelouga.BotGuild)
        await self.add_cog(Owner(self))#, guild=Botloader.BetaBelouga.BotGuild)
        await self.add_cog(Common(self))
        await self.add_cog(Admin(self))
        try:
            await self.add_cog(Music(self))
        except Exception as e: print(e)
        Botloader.Bot.console("INFO", f'Logged in as {self.user} (ID: {self.user.id})')
        await self.versions(type="on_ready", ctx=None)
        await self.change_presence(status=discord.Status.online, activity=discord.Game("Chargement des cookis!"))
        try:
            synced = await self.tree.sync()
            Botloader.Bot.console("INFO", f'Synced {len(synced)} commands')
        except Exception as e:
            Botloader.Bot.console("WARN", f'Error: {e}')
        statut = randint(0,1)
        if statut == 1:
            actype = discord.ActivityType.playing
        else:
            actype = discord.ActivityType.watching
        statut = statutpresence[statut]
        await self.change_presence(activity=discord.Activity(type=actype, name=statut))
        for command in self.commands:
            if command.help:
                self.command_descriptions[command.name] = command.help
        print("")


    async def versions(self, type, ctx: Context):
        patch = None
        if type == "on_ready":
            return Botloader.Bot.console("INFO", f'Logged in V{BOT_VERSION}')
        check = Version.check()
        if check == "j":
            description, color, url = "Votre bot est à jour.", discord.Colour.green(), "https://cdn3.emoji.gg/emojis/2990_yes.png"
            date, patch = Version.get_patch()
        elif check == "o":
            description, color, url = "Attention : votre bot n'est plus à jour !", discord.Colour.from_rgb(250, 0, 0), "https://cdn3.emoji.gg/emojis/1465-x.png"
            date, patch = Version.get_patch()
        else:
            description, color, url = "Attention : votre bot est en version bêta !", discord.Colour.orange(), "https://cdn3.emoji.gg/emojis/3235_warning2.png"
        if type == "commande":
            embed = discord.Embed(title="Notes de mise à jour", description=description, color=color)
            embed.set_thumbnail(url=url)
            embed.add_field(name="Version du bot :", value=BOT_VERSION, inline=False)
            embed.add_field(name="Dernière version :", value=Version.LASTER_VERSION, inline=False)
            if patch:
                embed.add_field(name=f"Patch Note {date} (dernière version stable):", value=patch, inline=False)
            return await ctx.reply(embed=embed)

    async def help(self, ctx: Context, args = None):
        if not args:
            embed = discord.Embed(title="Liste des commandes disponibles:", description="Certaines commandes ne sont pas recensées ici.", color=discord.Color.green())
            for command, description in self.command_descriptions.items():
                embed.add_field(name=f"{Botloader.Bot.Prefix}{command}", value=description, inline=False)
            await ctx.send(embed=embed)
        else:
            command_name = args[0]
            description = self.command_descriptions.get(command_name, "Aucune description disponible.")
            embed = discord.Embed(title=f"{Botloader.Bot.Prefix}{command_name}", description=description, color=discord.Color.green())
            await ctx.send(embed=embed)
    
    async def version(self, ctx: Context):
        await self.versions(type="commande", ctx=ctx)
        
    async def ping(self, ctx: Context):
        embed = discord.Embed(title="PONG", description=f":ping_pong: Le ping est de **{round(self.latency)}** secondes!")
        await ctx.send(embed=embed)
        
    async def restart(self, ctx: Context):
        if Botloader.owner_permission.check(ctx.author.id) != True:
            return await ctx.reply("Vous ne disposez pas des autorisations nécéssaire.")
        await ctx.send("Bot was offline for restart.")
        await asyncio.sleep(3)
        print("")
        Botloader.Bot.console("INFO", f'Bot Closed for restart')
        print("")
        global r
        r = "y"
        await self.close()


#gestion interaction boutons
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            await interaction.response.defer()
            if interaction.data["custom_id"] == "restart_test":
                view = discord.ui.View()
                item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Relancer le test", custom_id="restart_test", disabled=True)
                view.add_item(item=item)
                await interaction.channel.last_message.edit(view=view)
                ctx = Privat.ctx_mapping.get(interaction.user.id)
                lang, nombre = Privat.voca_user_data.get(interaction.user.id, "").split(",")
                return await Privat.test_voca_logic(self, ctx, lang, nombre)
            if interaction.data["custom_id"] == "spam_dm":
                b, guild, user, msg = interaction.data["values"][0].split("/|/")
                if b == "y":
                    data = Botloader.Data.get_user_conf(guild, interaction.user.id, Botloader.Data.cmd_value['blackliste_dm'])
                    if data is None:
                        Botloader.Data.insert_user_conf(guild, interaction.user.id, Botloader.Data.cmd_value['blackliste_dm'], user)
                    elif user not in data:
                        Botloader.Data.update_user_conf(guild, interaction.user.id, Botloader.Data.cmd_value['blackliste_dm'], data.append(user))
                    title = "Le message a bien été signalé et le membre bloqué.\nSi vous avez d'autre problèmes, n'ésitez pas à nous contacter:\nsupport@gamebot.smaugue.lol"
                    placeholder = "Signalé et Bloqué"
                else: 
                    title = "Le message a bien été signalé.\nSi vous avez d'autre problèmes, n'ésitez pas à nous contacter:\nsupport@gamebot.smaugue.lol"
                    placeholder = "Signalé"
                automod_channel_id = Botloader.Data.get_guild_conf(guild, 'automod_channel_report')
                try:
                    channel = bot.get_guild(int(guild)).get_channel(int(automod_channel_id))
                except Exception as e:
                    return await interaction.channel.send(f"Une erreur s'est produite: {e}. \n Veuillez contacter les administarteur du serveur don est issu le message ({ctx.guild})")
                startTime = datetime.strftime(datetime.now(Botloader.tz), '%H:%M:%S')
                embed = discord.Embed(title="Signalement de Spam en DM", description=startTime, color=discord.Color.brand_red())
                embed.add_field(name="User", value=bot.get_user(int(user)).mention, inline=False)
                embed.add_field(name="Target", value=interaction.user.mention, inline=False)
                embed.add_field(name="Message", value=msg, inline=False)
                embed.add_field(name="Etat de la modération:", value="En cour...", inline=False)
                view = discord.ui.View()
                item = discord.ui.Button(style=discord.ButtonStyle.danger, label="Modérer", custom_id="automod_action", disabled=False)
                view.add_item(item=item)
                await channel.send(embed=embed,view=view)
                view = discord.ui.View()
                item = discord.ui.Select(
                    custom_id='spam_dm',
                    placeholder=placeholder,
                    options=[
                        discord.SelectOption(label="empty", value=f"empty"),
                    ],
                    disabled=True
                )
                view.add_item(item=item)
                await interaction.message.edit(view=view)
                embed = discord.Embed(title="**Signalement**", description=title, color=discord.Colour.red())
                return await interaction.channel.send(embed=embed)
            if interaction.data["custom_id"] == "bugreport_correction" and interaction.user.id == Botloader.owner_permission.owner_id:
                view = discord.ui.View()
                item = discord.ui.Button(style=discord.ButtonStyle.gray, label="Corrigé", custom_id="bugreport_correction", disabled=True)
                view.add_item(item=item)
                embeds = interaction.message.embeds.copy()
                embed = embeds[0]
                embed.set_field_at(index=1, name=embed.fields[1].name, value="Corrigé.", inline=embed.fields[1].inline)
                embed.color = discord.Color.green()
                return await interaction.message.edit(embed=embed, view=view)
            if interaction.data["custom_id"] == "bugreport_correction_n" and interaction.user.id == Botloader.owner_permission.owner_id:
                view = discord.ui.View()
                item = discord.ui.Button(style=discord.ButtonStyle.gray, label="Non Recevable", custom_id="bugreport_correction_n", disabled=True)
                view.add_item(item=item)
                embeds = interaction.message.embeds.copy()
                embed = embeds[0]
                embed.set_field_at(index=1, name=embed.fields[1].name, value="Non Recevable.", inline=embed.fields[1].inline)
                embed.color = discord.Color.dark_gray()
                return await interaction.message.edit(embed=embed, view=view)
            if interaction.data["custom_id"] == "automod_action":
                view = discord.ui.View()
                item = discord.ui.Button(style=discord.ButtonStyle.success, label="Modéré", custom_id="automod_action", disabled=True)
                view.add_item(item=item)
                embeds = interaction.message.embeds.copy()
                embed = embeds[0]
                embed.set_field_at(index=3, name=embed.fields[3].name, value=f"Modéré par {interaction.user.mention}.", inline=embed.fields[1].inline)
                embed.color = discord.Color.dark_red()
                return await interaction.message.edit(embed=embed, view=view)
            if interaction.data["custom_id"] == "test_1":
                selected_option = interaction.data["values"][0]
                await interaction.channel.send(selected_option)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        blw, blws = AutoMod.check_message(message.content)
        if len(blw) != 0:
            automod_channel_id = Botloader.Data.get_guild_conf(message.guild.id, 'automod_channel_report')
            if automod_channel_id is not None:
                channel = message.guild.get_channel(int(automod_channel_id))
                if channel:
                    if isinstance(message.channel, discord.channel.DMChannel):
                        zone = "Signalement de langage offensant en DM."
                    else:
                        zone = "Signalement de langage offensant."
                    startTime = datetime.strftime(datetime.now(Botloader.tz), '%H:%M:%S')
                    embed = discord.Embed(title=zone, description=startTime, color=discord.Color.brand_red())
                    embed.set_thumbnail(url=message.author.avatar.url)
                    embed.add_field(name="User", value=message.author.mention, inline=False)
                    embed.add_field(name="Channel & Link", value=message.jump_url, inline=False)
                    embed.add_field(name="Message", value=message.content, inline=False)
                    embed.add_field(name="Etat de la modération:", value="En cour...", inline=False)
                    view = discord.ui.View()
                    item = discord.ui.Button(style=discord.ButtonStyle.danger, label="Modérer", custom_id="automod_action", disabled=False)
                    view.add_item(item=item)
                    for key in blw:
                        embed.add_field(name=f"Mot {key} détecté:", value=f"{round(blws[key], 2) * 100}% de ressemblance avec **{blw[key]}**.", inline=False)
                    if message.attachments:
                        for attachment in message.attachments:
                            embed.add_field(name="Attachment", value=attachment.proxy_url, inline=False)
                    if channel.id == Botloader.GameHub.MessageChannel:
                        await channel.send("||<@575746878583472128>||||<@724996627366019133>||", embed=embed, view=view)
                    else:
                        await channel.send(embed=embed, view=view)
        data = Botloader.Data.get_guild_conf(message.guild.id, Botloader.Data.guild_conf['command_name'])
        if data:
            if len(data) > 0:
                data = data.split("\n")
            ctx = await bot.get_context(message)
            if message.content in data:
                executor = Botloader.Data.get_guild_conf(message.guild.id, message.content)
                try:
                    action_list = parse_actions(ctx, executor)
                    for action in action_list:
                        await action.execute(ctx)
                except Exception as e:
                    await ctx.send(f"Error: {str(e)}")
        #lvtts
        if message.channel.id == 1242185337053380738:
            if Botloader.Data.get_user_conf(message.guild.id, message.author.id, Botloader.Data.cmd_value['vtts_l']) != "1":
                await Botloader.Bot.on_refus_interaction(ctx)
            else:
                M = await ctx.reply("En cours de validation...", mention_author=False)
                try:
                    if len(blw) != 0:
                        await M.edit(content="Échec de la validation: surveillez votre langage.")
                    elif ctx.voice_client is None:
                        await M.edit(content=f"Le bot n'est pas connecté à un canal vocal. Utilisez {Botloader.Bot.Prefix}join pour lui faire rejoindre.")
                    else:
                        try:
                            startTime = datetime.strftime(datetime.now(Botloader.tz), '%H:%M:%S')
                            txt = message.content
                            tts = gTTS(text=txt, lang="fr")
                            output_filename = f'{ctx.guild.id}_{startTime}_output.mp3'
                            
                            if os.path.exists(output_filename):
                                i = 2
                                while os.path.exists(f'{ctx.guild.id}_{startTime}_{i}_output.mp3'):
                                    i += 1
                                output_filename = f'{ctx.guild.id}_{startTime}_{i}_output.mp3'
                            
                            tts.save(output_filename)
                            await Botloader.Bot.play_audio(ctx, output_filename)
                            await M.edit(content="Succès.")
                        except Exception as e:
                            await M.edit(content=f"Une erreur est survenue: {str(e)} \n N'hésitez pas à faire un `/bugreport`")
                except Exception as e:
                    print(e)
#       else:
#           count = 0
#           if message.attachments:
#               count = 5
#           for char in message.content:
#               if char != ' ':
#                   count += 1
#           data = Botloader.Data.get_user_conf(message.guild.id, message.author.id, 'xp_reward_total')
#           data_m = Botloader.Data.get_user_conf(message.guild.id, message.author.id, 'xp_reward_message')
#           xp_multiplicator = Botloader.Data.get_guild_conf(message.guild.id, Botloader.Data.guild_conf['xp_message_by_character'])
#           if xp_multiplicator is None:
#               xp_multiplicator = 1
#           else:
#               xp_multiplicator = float(xp_multiplicator)
#           if data is None:
#               Botloader.Data.insert_user_conf(message.guild.id, message.author.id, 'actual_xp_level', 0)
#               Botloader.Data.insert_user_conf(message.guild.id, message.author.id, 'xp_reward_message', 0)
#               Botloader.Data.insert_user_conf(message.guild.id, message.author.id, 'xp_reward_vocal', 0)
#               Botloader.Data.insert_user_conf(message.guild.id, message.author.id, 'xp_reward_total', 0)
#               data = 0
#               data_m = 0
#           else:
#               data = float(data)
#               data_m = float(data_m)
#           Botloader.Data.update_user_conf(message.guild.id, message.author.id, 'xp_reward_message', data_m + count * xp_multiplicator)
#           Botloader.Data.update_user_conf(message.guild.id, message.author.id, 'xp_reward_total', data + count * xp_multiplicator)
#            await message.reply(f'Vous avez gagné {count * xp_multiplicator}. Vous avez un total de {data + count * xp_multiplicator} dont {data_m + count * xp_multiplicator} grâce aux messages.')
        await self.process_commands(message)

bot = client = BotClient(command_prefix=Botloader.Bot.Prefix,intents=discord.Intents.all(),description="Belouga.exe is watching you!!!")
bot.remove_command('help')

@bot.command(name="restart")
async def restart(ctx):
    await bot.restart(ctx)
    
@bot.command(name="ping")
async def ping(ctx):
    await bot.ping(ctx)

@bot.hybrid_command(name="version")
async def version(ctx):
    await bot.version(ctx)

@bot.hybrid_command(name="help")
async def help(ctx):
    await bot.help(ctx)

@bot.event
async def on_error(event_method, *args, **kwargs):
    error = kwargs.get('error')
    if not error:
        return
    guild = bot.get_guild(Botloader.Bot.BotGuild)
    channel = guild.get_channel_or_thread(Botloader.Bot.BugReportChannel)
    embed = discord.Embed(title="Rapport de Bug Global",description=f"Une erreur est survenue au niveau de: `{event_method}`.",colour=discord.Colour.orange())
    embed.add_field(name="Bug:", value=str(error), inline=False)
    embed.add_field(name="Etat de correction:", value="En cour...", inline=False)
    embed.set_author(name="Rapport Automatique", icon_url=bot.user.avatar.url)
    view = discord.ui.View()
    item = discord.ui.Button(style=discord.ButtonStyle.green, label="Corriger", custom_id="bugreport_correction")
    view.add_item(item=item)
    item = discord.ui.Button(style=discord.ButtonStyle.grey, label="Non Recevable", custom_id="bugreport_correction_n")
    view.add_item(item=item)
    await channel.send(embed=embed, view=view)

@bot.event
async def on_command_error(ctx: Context, error):
    command = ctx.command.qualified_name if ctx.command else "Unknown command"
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.reply("Missing Argument", ephemeral=True)
    if isinstance(error, commands.CommandNotFound):
        return await ctx.reply("Command no found.", ephemeral=True)
    if isinstance(error, commands.MissingPermissions):
        return await ctx.reply('Missing permissions.', ephemeral=True)
    if isinstance(error, discord.Forbidden):
        return await ctx.reply('Missing permissions.', ephemeral=True)
    if isinstance(error, discord.NotFound):
        return await ctx.reply('Discord possède une API de piètre qualité.')
    guild = bot.get_guild(Botloader.Bot.BotGuild)
    channel = guild.get_channel_or_thread(Botloader.Bot.BugReportChannel)
    embed = discord.Embed(title="Rapport de Bug",description=f"Commande concernée `{command}`.",colour=discord.Colour.orange())
    embed.add_field(name="Bug:", value=str(error), inline=False)
    embed.add_field(name="Etat de correction:", value="En cour...", inline=False)
    embed.set_author(name="Rapport Automatique", icon_url=bot.user.avatar.url)
    view = discord.ui.View()
    item = discord.ui.Button(style=discord.ButtonStyle.green, label="Corriger", custom_id="bugreport_correction")
    view.add_item(item=item)
    item = discord.ui.Button(style=discord.ButtonStyle.grey, label="Non Recevable", custom_id="bugreport_correction_n")
    view.add_item(item=item)
    await channel.send(embed=embed, view=view)
    await ctx.reply('Une erreur est survenue et a été signalé.')

try:
    bot.run(Botloader.Bot.Token)
except: print("Bad Pasword")
os.system(f"python Launcher.py --bot {Botloader.Bot.Name} --restart {r} --pasword {Botloader.Bot.Pasword}")