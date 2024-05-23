from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from typing import List
import discord
import Botloader

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def blackliste_autocompletion(self, interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
        commands = ['sayic', 'say', 'dm', 'vtts', 'ftts', 'rdm']
        return [
                app_commands.Choice(name=cmd, value=cmd)
                for cmd in commands if current.lower() in cmd.lower()
            ]
    
    async def srvconf_autocompletion(self, interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
        parametres = ['xp_message_by_character', 'xp_vocal_by_minute']
        return [
                app_commands.Choice(name=parametre, value=parametre)
                for parametre in parametres if current.lower() in parametre.lower()
            ]

    @commands.hybrid_command(name="blackliste")
    @commands.has_permissions(administrator = True)
    @app_commands.autocomplete(cmd = blackliste_autocompletion)
    async def blackliste(self, ctx: Context, member: discord.Member, cmd, permission: bool):
        var_key = Botloader.Data.cmd_value[cmd]
        data = Botloader.Data.get_user_conf(ctx.guild.id, ctx.author.id, cmd)
        if data is not None:
            try:
                Botloader.Data.update_user_conf(ctx.guild.id,member.id,var_key,permission)
                return await ctx.reply(f"Membre {member} ajouté à la blackliste de la command {cmd} (précédemment {data}).")
            except Exception as e:
                return await ctx.reply(f"Erreur: {e}.")
        try:
            Botloader.Data.insert_user_conf(guild_id=ctx.guild.id, user_id=member.id, conf_key=var_key, conf_value=permission)
            return await ctx.reply(f"Membre {member} ajouté à la blackliste de la command {cmd}.")
        except Exception as e:
            return await ctx.reply(f"Erreur: {e}.")

    @commands.hybrid_command(name="clear", help=f"Supprime les n derniers messages dans le canal.\nSyntaxe: `{Botloader.Bot.Prefix}clear [argument(int)]`")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: Context, amount):
        try:
            await ctx.channel.purge(limit=int(amount))
            return await ctx.send("Succès.", ephemeral=True)
        except ValueError:
            return await ctx.reply('Veuillez entrer un entier valide comme argument.')
        
    @commands.hybrid_command(name="srvconf")
    @commands.has_permissions(administrator = True)
    @app_commands.autocomplete(parametre=srvconf_autocompletion)
    async def serverconf(self, ctx: Context, parametre: str, valeur: str):
        data = Botloader.Data.get_guild_conf(ctx.guild.id, Botloader.Data.guild_conf[parametre])
        if data is not None:
            try:
                Botloader.Data.update_guild_conf(ctx.guild.id, Botloader.Data.guild_conf[parametre], valeur)
                return await ctx.reply(f"Le paramètre {parametre} a bien été modifié: {data} => {valeur}.")
            except Exception as e:
                return await ctx.reply(f"Erreur: {e}.")
        try:
            Botloader.Data.insert_guild_conf(ctx.guild.id, Botloader.Data.guild_conf[parametre], valeur)
            return await ctx.reply(f"Le paramètre {parametre} a bien été définit sur {valeur}.")
        except Exception as e:
            return await ctx.reply(f"Erreur: {e}.")
