import discord
import asyncio
import aiohttp
from Packs.Botloader import Data, Bot
from discord.ui import View, Select
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from typing import List
from Packs.interpretor import parse_actions

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def blackliste_autocompletion(self, interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
        commands = ['sayic', 'say', 'dm', 'vtts', 'ftts', 'random', 'execute']
        return [
                app_commands.Choice(name=cmd, value=cmd)
                for cmd in commands if current.lower() in cmd.lower()
            ]
    
    async def srvconf_autocompletion(self, interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
        parametres = ['automod_channel']
        return [
                app_commands.Choice(name=parametre, value=parametre)
                for parametre in parametres if current.lower() in parametre.lower()
            ]

    @commands.hybrid_command(name="blackliste")
    @commands.has_permissions(administrator = True)
    @app_commands.autocomplete(cmd = blackliste_autocompletion)
    @commands.guild_only()
    async def blackliste(self, ctx: Context, member: discord.Member, cmd, permission: bool):
        if cmd not in Data.key:
            return await ctx.reply("Clef non-valide", ephemeral=True)
        var_key =Data.key[cmd]
        data = Data.get_user_conf(ctx.guild.id, ctx.author.id, cmd)
        if data is not None:
            try:
                Data.set_user_conf(ctx.guild.id,member.id,var_key,permission)
                return await ctx.reply(f"Membre {member} ajouté à la blackliste de la command {cmd} (précédemment {data}).")
            except Exception as e:
                return await ctx.reply(f"Erreur: {e}.")
        try:
            Data.set_user_conf(guild_id=ctx.guild.id, user_id=member.id, conf_key=var_key, conf_value=permission)
            return await ctx.reply(f"Membre {member} ajouté à la blackliste de la command {cmd}.")
        except Exception as e:
            return await ctx.reply(f"Erreur: {e}.")

#    @commands.hybrid_command(name="permission")
#    @commands.has_permissions(administrator = True)
#    @app_commands.autocomplete(cmd = blackliste_autocompletion)
#    @commands.guild_only()
#    async def permission(self, ctx: Context, member: discord.member):
#        bot = self.bot
#        embed = discord.Embed(title="**Permission du membre:**",description="Permissions accordées au membre.",color=discord.Colour.dark_magenta())
#        commands_list = []
#        data = Botloader.Data.get_user_conf(ctx.guild.id, ctx.author.id, 'cmd')
#        if data and len(data) > 0:
#            data = data.split("\n")
#            for command in data:
#                commands_list.append(command)
#                embed.add_field(name=command, value=Botloader.Data.get_guild_conf(ctx.guild.id, command), inline=False)
#        else:
#            embed.add_field(name="Aucune commande custom disponible pour ce serveur.",value="Créez en avec `/create_command <prefix> <name>`.",inline=False)
#
#        class CommandSelect(Select):
#            def __init__(self, commands):
#                options = [discord.SelectOption(label=cmd, description=f"Select {cmd}") for cmd in commands]
#                super().__init__(placeholder="Sélectionnez une commande", min_values=1, max_values=1, options=options)
#                self.selected_command = None
#            async def callback(self, interaction: discord.Interaction):
#                self.selected_command = self.values[0]
#                self.view.stop()
#        class CommandSelectView(View):
#            def __init__(self, commands, timeout=60):
#                super().__init__(timeout=timeout)
#                self.command_select = CommandSelect(commands)
#                self.add_item(self.command_select)
#            async def on_timeout(self):
#                for item in self.children:
#                    item.disabled = True
#                await self.message.edit(view=self)
#        if commands_list:
#            view = CommandSelectView(commands_list)
#            message = view.message = await ctx.reply(embed=embed, view=view)
#            await view.wait()

    @commands.hybrid_command(name="clear", help=f"Supprime les n derniers messages dans le canal.\nSyntaxe: `{Bot.Prefix}clear [argument(int)]`")
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def clear(self, ctx: Context, amount: int):
        try:
            await ctx.channel.purge(limit=int(amount))
            return await ctx.send("Succès.", ephemeral=True)
        except ValueError:
            return await ctx.reply('Veuillez entrer un entier valide comme argument.')
        except discord.NotFound:
            return

    @commands.hybrid_command(name="automod_channel")
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def automod_channel(self, ctx: Context, channel: discord.TextChannel):
        data = Data.get_guild_conf(ctx.guild.id, Data.AUTOMOD_CHANNEL)
        if data is not None:
            try:
                Data.set_guild_conf(ctx.guild.id, Data.AUTOMOD_CHANNEL, channel.id)
                return await ctx.reply(f"Le channel automod a bien été modifié: <#{data}> => {channel}.")
            except Exception as e:
                return await ctx.reply(f"Erreur: {e}.")
        try:
            Data.set_guild_conf(ctx.guild.id, Data.AUTOMOD_CHANNEL, channel.id)
            return await ctx.reply(f"Le channel automod a bien été définit sur {channel}.")
        except Exception as e:
            return await ctx.reply(f"Erreur: {e}.")
        
    @commands.hybrid_command(name="automod_level", help = "Définit la sensibilité de l'automod 1 = insultes graves uniquement, 3 = langage grossier inclu.")
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def automod_level(self, ctx: Context, level = 3):
        data = Data.get_guild_conf(ctx.guild.id, Data.AUTOMOD_LEVEL)
        if data is not None:
            try:
                Data.set_guild_conf(ctx.guild.id, Data.AUTOMOD_LEVEL, level)
                return await ctx.reply(f"La puissance de l'automod a bien été modifié: {data} => {level}.")
            except Exception as e:
                return await ctx.reply(f"Erreur: {e}.")
        try:
            Data.set_guild_conf(ctx.guild.id, Data.AUTOMOD_LEVEL, level)
            return await ctx.reply(f"La puissance de l'automod a bien été définit sur {level}.")
        except Exception as e:
            return await ctx.reply(f"Erreur: {e}.")
    
    @commands.hybrid_command(name="execute")
    @commands.guild_only()
    async def execute(self, ctx: Context,*,actions: str):
        if Data.get_user_conf(ctx.guild.id, ctx.author.id, Data.key_value['execute']) == "1":
            try:
                action_list = parse_actions(ctx, actions)
                for action in action_list:
                    await action.execute(ctx)
            except Exception as e:
                await ctx.send(f"Error: {str(e)}")
                Bot.console('ERROR', e)
        else: await Bot.on_refus_interaction(ctx)

    @commands.hybrid_command(name="create_command")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def create_command(self, ctx: commands.Context, prefix: str, name: str):
        # Init
        data = Data.get_guild_conf(ctx.guild.id, Data.CUSTOM_COMMANDS_NAMES)
        if data and len(data) > 0:
            data = data.split("\n")
            if len(data) > 4:
                return await ctx.reply("Vous avez atteins le nombre maximum de commande custom.")
        executore = "Start{}"
        embed = discord.Embed(title="**Commande Personnalisée**", description=name, color=discord.Colour.dark_magenta())
        embed.add_field(name="Prefixe", value=prefix)
        bot = self.bot
        command_name = f"{prefix}{name}"
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
                    for item in self.children:
                        if isinstance(item, discord.ui.Button):
                            item.disabled = True
                    self.embed.add_field(name="Executor:", value=self.executore, inline=False)
                    await interaction.edit_original_response(embed=self.embed, view=self)
                    if self.data:
                        if command_name in self.data:
                            return await ctx.send('La command existe déjà.')
                        data_str = "\n".join(self.data)
                    else:
                        data_str = ""
                    data = data_str+"\n"+command_name
                    Data.set_guild_conf(ctx.guild.id, Data.CUSTOM_COMMANDS_NAMES, data)
                    Data.set_guild_conf(ctx.guild.id,command_name, self.executore)
                    return await ctx.send('Enregistré')
        view = ActionSelector(self.bot)
        await ctx.send(embed=embed, view=view)
    
    @commands.hybrid_command(name="custom_commands")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def custom_commands(self, ctx: commands.Context):
        bot = self.bot
        data = Data.get_guild_conf(ctx.guild.id, Data.key_value['custom_commands_names'])
        embed = discord.Embed(title="**Liste des Commandes Personnalisées**",description="Liste des commandes personnalisées du serveur.",color=discord.Colour.dark_magenta())
        commands_list = None
        if data and len(data) > 0:
            data = data.split("\n")
            for command in data:
                commands_list = []
                commands_list.append(command)
                embed.add_field(name=command, value=Data.get_guild_conf(ctx.guild.id, command), inline=False)
        else:
            embed.add_field(name="Aucune commande custom disponible pour ce serveur.",value="Créez en avec `/create_command <prefix> <name>`.",inline=False)
            return await ctx.reply(embed=embed)

        class CommandSelect(Select):
            def __init__(self, commands):
                options = [discord.SelectOption(label=cmd, description=f"Select {cmd}") for cmd in commands]
                super().__init__(placeholder="Sélectionnez une commande", min_values=1, max_values=1, options=options)
                self.selected_command = None
            async def callback(self, interaction: discord.Interaction):
                self.selected_command = self.values[0]
                self.view.stop()
        class CommandSelectView(View):
            def __init__(self, commands, timeout=60):
                super().__init__(timeout=timeout)
                self.command_select = CommandSelect(commands)
                self.add_item(self.command_select)
            async def on_timeout(self):
                for item in self.children:
                    item.disabled = True
                await self.message.edit(view=self)
        if commands_list:
            view = CommandSelectView(commands_list)
            message = view.message = await ctx.reply(embed=embed, view=view)
            await view.wait()
            selected_command = view.command_select.selected_command
            if selected_command:
                class ActionSelector(View):
                    def __init__(self, bot, selected_command, timeout=60):
                        super().__init__(timeout=timeout)
                        self.bot = bot
                        self.selected_command = selected_command
                        self.embed = embed
                        self.data = data
                    @discord.ui.button(style=discord.ButtonStyle.red, label=f"Supprimer {selected_command}", custom_id="delete_command")
                    async def delete_button(self, button: discord.ui.Button, interaction: discord.Interaction):
                        button, interaction = interaction, button
                        button.disabled = True
                        for item in self.children:
                            if isinstance(item, discord.ui.Button):
                                item.disabled = True
                        await interaction.edit_original_response(embed=self.embed, view=self)
                        await ctx.reply(f"Confirmez la suppression de `{self.selected_command}` avec `delete` ou annulez avec `cancel`.", ephemeral=True)
                        try:
                            user_message = await bot.wait_for(
                                "message",
                                timeout=60,
                                check=lambda m: m.author == interaction.user and m.channel == interaction.channel
                            )
                            if user_message.content.lower() == "delete":
                                self.data.remove(selected_command)
                                data_str = "\n".join(self.data)
                                Data.set_guild_conf(ctx.guild.id, Data.key_value['custom_commands_names'], data_str)
                                Data.delete_guild_conf(ctx.guild.id, selected_command)
                                await user_message.reply(f"La commande `{self.selected_command}` a été supprimée.")
                                await user_message.delete()
                                return
                            elif user_message.content.lower() == "cancel":
                                await user_message.reply("Suppression annulée.")
                                await user_message.delete()
                                return
                            else:
                                await user_message.reply("Commande non reconnue. Annulation de la suppression.")
                                await user_message.delete()
                                return
                        except asyncio.TimeoutError:
                            return await ctx.send("Temps écoulé. Veuillez réessayer.")
                    @discord.ui.button(style=discord.ButtonStyle.gray, label="Annuler", custom_id="ok")
                    async def ok_button(self, button: discord.ui.Button, interaction: discord.Interaction):
                        button, interaction = interaction, button
                        button.disabled = True
                        for item in self.children:
                            if isinstance(item, discord.ui.Button):
                                item.disabled = True
                        return await interaction.edit_original_response(embed=self.embed, view=self)
                await message.edit(embed=embed, view=ActionSelector(self, selected_command))
            else:
                await ctx.send("Temps écoulé. Veuillez réessayer.")
        else:
            await ctx.reply(embed=embed)
