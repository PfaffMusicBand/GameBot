import discord
import asyncio
import aiohttp
from Packages import Botloader
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from typing import List
from Packages.interpretor import parse_actions

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
        parametres = ['xp_message_by_character', 'xp_vocal_by_minute', 'automod_channel']
        return [
                app_commands.Choice(name=parametre, value=parametre)
                for parametre in parametres if current.lower() in parametre.lower()
            ]

    @commands.hybrid_command(name="blackliste")
    @commands.has_permissions(administrator = True)
    @app_commands.autocomplete(cmd = blackliste_autocompletion)
    @commands.guild_only()
    async def blackliste(self, ctx: Context, member: discord.Member, cmd, permission: bool):
        if cmd not in Botloader.Data.cmd_value:
            return await ctx.reply("Clef non-valide", ephemeral=True)
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
    @commands.guild_only()
    async def clear(self, ctx: Context, amount: int):
        try:
            await ctx.channel.purge(limit=int(amount))
            return await ctx.send("Succès.", ephemeral=True)
        except ValueError:
            return await ctx.reply('Veuillez entrer un entier valide comme argument.')

    @commands.hybrid_command(name="srvconf")
    @commands.has_permissions(administrator = True)
    @app_commands.autocomplete(parametre=srvconf_autocompletion)
    @commands.guild_only()
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
    
    @commands.hybrid_command(name="execute")
    @commands.guild_only()
    async def execute(self, ctx: Context,*,actions: str):
        if Botloader.Data.get_user_conf(ctx.guild.id, ctx.author.id, Botloader.Data.cmd_value['execute']) == "1":
            try:
                action_list = parse_actions(ctx, actions)
                for action in action_list:
                    await action.execute(ctx)
            except Exception as e:
                await ctx.send(f"Error: {str(e)}")
        else: await Botloader.Bot.on_refus_interaction(ctx)

    @commands.hybrid_command(name="create_command")
    @commands.guild_only()
    async def create_command(self, ctx: commands.Context, prefix: str, name: str):
        # Init
        executore = "Start{}"
        embed = discord.Embed(title="**Commande Personnalisée**", description=name, color=discord.Colour.dark_magenta())
        embed.add_field(name="Prefixe", value=prefix)
        bot = self.bot
        command_name = f"{prefix}{name}"
        data = Botloader.Data.get_guild_conf(ctx.guild.id, Botloader.Data.guild_conf['command_name'])
        if data and len(data) > 0:
            data = data.split("\n")
        # Button
        class ActionSelector(discord.ui.View):
            def __init__(self, bot, timeout=60):
                super().__init__(timeout=timeout)
                self.bot = bot
                self.embed = embed
                self.data = data
                self.executore = executore
                self.message_button_disabled = False
                self.image_button_disabled = False
                self.ok_button_disabled = False

            @discord.ui.button(style=discord.ButtonStyle.blurple, label="Envoyer un message", custom_id="message")
            async def send_message_button(self, button: discord.ui.Button, interaction: discord.Interaction):
                button, interaction = interaction, button
                if not self.message_button_disabled:
                    self.message_button_disabled = True
                    button.disabled = True
                    await interaction.response.edit_message(embed=self.embed, view=self)

                M1 = await interaction.channel.send(f"{interaction.user.mention}, veuillez saisir le message à envoyer :")
                try:
                    user_message = await bot.wait_for(
                        "message",
                        timeout=60,
                        check=lambda m: m.author == interaction.user and m.channel == interaction.channel
                    )
                    self.embed.add_field(name="Message", value=user_message.content, inline=False)
                    self.executore = f"{self.executore}&SendMessage{{{user_message.content}}}"
                    await interaction.edit_original_response(embed=self.embed, view=self)
                    await user_message.delete()
                    await M1.delete()
                except asyncio.TimeoutError:
                    await interaction.followup.send("Temps écoulé. Veuillez réessayer.")

            @discord.ui.button(style=discord.ButtonStyle.green, label="Envoyer une image", custom_id="image")
            async def send_image_button(self, button: discord.ui.Button, interaction: discord.Interaction):
                button, interaction = interaction, button
                if not self.image_button_disabled:
                    self.image_button_disabled = True
                    button.disabled = True
                    await interaction.response.edit_message(embed=self.embed, view=self)

                M1 = await interaction.channel.send(f"{interaction.user.mention}, veuillez envoyer l'url de l'image :")
                try:
                    user_message = await bot.wait_for(
                        "message",
                        timeout=60,
                        check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
                    url = user_message.content
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            if response.status == 200:
                                self.executore = f"{self.executore}&SendImage{{{url}}}"
                                self.embed.add_field(name="Image", value=url, inline=False)
                                await interaction.edit_original_response(embed=self.embed, view=self)
                                await user_message.delete()
                                await M1.delete()
                            else:
                                ctx.reply("Aucunne image disponible.", ephemeral=True)
                                self.image_button_disabled = False
                                button.disabled = False
                                await interaction.edit_original_response(embed=self.embed, view=self)
                except aiohttp.ClientConnectorError:
                    await ctx.reply("URL incoreccte.")
                    self.image_button_disabled = False
                    button.disabled = False
                    await interaction.edit_original_response(embed=self.embed, view=self)
                except asyncio.TimeoutError:
                    await interaction.followup.send("Temps écoulé. Veuillez réessayer.")
            
            @discord.ui.button(style=discord.ButtonStyle.gray, label="Terminer", custom_id="ok")
            async def ok_button(self, button: discord.ui.Button, interaction: discord.Interaction):
                button, interaction = interaction, button
                if not self.ok_button_disabled:
                    self.ok_button_disabled = True
                    button.disabled = True
                    self.embed.add_field(name="Executor:", value=self.executore, inline=False)
                    await interaction.edit_original_response(embed=self.embed, view=self)
                    if self.data:
                        if command_name in self.data:
                            return await ctx.send('La command existe déjà.')
                        else:
                            data_str = "\n".join(self.data)
                            data = data_str+"\n"+command_name
                            Botloader.Data.update_guild_conf(ctx.guild.id, Botloader.Data.guild_conf['command_name'], data)
                            Botloader.Data.insert_guild_conf(ctx.guild.id,command_name, self.executore)
                            return await ctx.send('Enregistré')
                    else:
                        Botloader.Data.insert_guild_conf(ctx.guild.id, Botloader.Data.guild_conf['command_name'], command_name)
                        print(self.executore)
                        Botloader.Data.insert_guild_conf(ctx.guild.id,command_name, self.executore)
                        return await ctx.send('Enregistré')

        # Suite
        view = ActionSelector(self.bot)
        await ctx.send(embed=embed, view=view)