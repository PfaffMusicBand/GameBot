import discord
import asyncio
import os
from random import randint
from typing import Any
from discord.ext import commands
from datetime import datetime
import Botloader
import argparse
from common import Common
from privat import Privat
from owner import Owner
from discord.ext.commands import Context

def main():
    parser = argparse.ArgumentParser(description='Scripte Bot V1.2')
    parser.add_argument('Botname', type=str, default="Bot", help='Nom du bot à lancer')
    args = parser.parse_args()
    Botloader.Bot.Launched(args.Botname)

if __name__ == '__main__':
    main()

statutpresence = ["you!", "cooked you!"]
botversion = 1.4
r = "n"

class BotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_descriptions = {}

    async def on_ready(self):
        await self.add_cog(Common(self))
        await self.add_cog(Privat(self))
        await self.add_cog(Owner(self))
        #await self.add_cog(Admin(self))
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
        while True:
            h, m, s = datetime.strftime(datetime.now(), '%H'), datetime.strftime(datetime.now(), '%M'), datetime.strftime(datetime.now(), '%S')
            if h == m and h == s:
                guild = self.get_guild(Botloader.Bot.BotGuild)
                channel = guild.get_channel_or_thread(Botloader.Bot.AnnonceChannel)
                ping = await channel.send(f"@here il est {h}h{m}")
                await ping.publish()
                await asyncio.sleep(60-(int(s)-1))
                ping = await channel.send("Trop tard!")
                await ping.publish()
            await asyncio.sleep(1)

    async def versions(self, type, ctx: Context):
        if botversion == float(Botloader.version.recommanded):
            description, color, url = "Votre bot est à jour.", discord.Colour.green(), "https://cdn3.emoji.gg/emojis/2990_yes.png"
        elif botversion < float(Botloader.version.recommanded):
            description, color, url = "Attention : votre bot n'est plus à jour !", discord.Colour.from_rgb(250, 0, 0), "https://cdn3.emoji.gg/emojis/1465-x.png"
        else:
            description, color, url = "Attention : votre bot est en version bêta !", discord.Colour.orange(), "https://cdn3.emoji.gg/emojis/3235_warning2.png"
        if type == "commande":
            embed = discord.Embed(title="Notes de mise à jour", description=description, color=color)
            embed.set_thumbnail(url=url)
            embed.add_field(name="Version du bot :", value=botversion, inline=False)
            embed.add_field(name="Version recommandée :", value=Botloader.version.recommanded, inline=False)
            embed.add_field(name="Dernière version :", value=Botloader.version.recommanded, inline=False)
            await ctx.channel.send(embed=embed)
        if type == "on_ready":
            Botloader.Bot.console("INFO", f'Logged in V{botversion}')
            
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
        embed = discord.Embed(title="PONG", description=f":ping_pong: Le ping est de **{round(self.bot.latency)}** secondes!")
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

    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            if interaction.data["custom_id"] == "restart_test":
                view = discord.ui.View()
                item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Relancer le test", custom_id="restart_test", disabled=True)
                view.add_item(item=item)
                await interaction.channel.last_message.edit(view=view)
                ctx = Privat.ctx_mapping.get(interaction.user.id)
                lang, nombre = Privat.voca_user_data.get(interaction.user.id, "").split(",")
                await Privat.test_voca_logic(self, ctx, lang, nombre)
                return
            if interaction.data["custom_id"] == "Spam":
                view = discord.ui.View()
                item = discord.ui.Button(style=discord.ButtonStyle.danger, label="Signaler un Spam", custom_id="dm_spam", disabled=True)
                view.add_item(item=item)
                await interaction.message.edit(view=view)
                embed = discord.Embed(title="**Signalement**", description="Le message a bien été signalé.", color=discord.Colour.red())
                await interaction.response.send_message(embed=embed)
                return

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id or message is discord.Interaction:
            pass
        else:
            blw, blws = Botloader.auto_mod.check_message(message.content)
            if len(blw) != 0:
                guild = self.get_guild(Botloader.Bot.BotGuild)
                channel = guild.get_channel(Botloader.Bot.MessageChannel)
                startTime = datetime.strftime(datetime.now(), '%H:%M:%S')
                if isinstance(message.channel, discord.channel.DMChannel):
                    zone = "DM"
                else:
                    zone = "Serveur"
                embed = discord.Embed(title=zone, description=startTime, color=discord.Color.brand_red())
                embed.set_thumbnail(url=message.author.avatar)
                embed.add_field(name="User", value=message.author.mention, inline=False)
                embed.add_field(name="Server", value=message.guild, inline=False)
                embed.add_field(name="Channel & Link", value=message.jump_url, inline=False)
                embed.add_field(name="Message", value=message.content, inline=False)
                for key in blw:
                    embed.add_field(name=f"Mot {key} détecté:", value=f"{round(blws[key], 2)*100}% de resemblance avec **{blw[key]}**.", inline=False)
                if message.attachments:
                    for attachment in message.attachments:
                        embed.add_field(name="Attachment", value=attachment.proxy_url, inline=False)
                await channel.send(embed=embed)
        await self.process_commands(message)

bot = BotClient(command_prefix=Botloader.Bot.Prefix, intents=discord.Intents.all(), description="Belouga.exe is watching you!!!")
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

bot.run(Botloader.Bot.Token)
os.system(f"python Launcher.py --bot {Botloader.Bot.Name} --version {botversion} --restart {r}")