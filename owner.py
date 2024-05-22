import discord
from discord.ext import commands
from discord.ext.commands import Context
import Botloader
import asyncio

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        Owner.app_command.deleter
        
    @commands.command(name="addtoliste", )
    async def addtoliste(self, ctx: Context, member: discord.Member, variable, value):
        if not Botloader.owner_permission.check(ctx.author.id):
            return
        try:
            Botloader.Data.insert_user_conf(guild_id=ctx.guild.id, user_id=member.id, category=Botloader.Data.user_category['permission'], variable_key=variable, variable_value=value)
            await ctx.reply(f"Membre {member} ajouté à la liste {variable} avec la valeur {value}")
        except Exception as e:
            await ctx.reply(f"Erreur: {e}.")

    @commands.command(name="deletetoliste")
    async def deletetoliste(self, ctx: Context, member: discord.Member, variable):
        if not Botloader.owner_permission.check(ctx.author.id):
            return
        try:
            value = Botloader.Data.get_user_conf(guild_id=ctx.guild.id, user_id=member.id, category=Botloader.Data.user_category['permission'], variable_key=variable)
            Botloader.Data.delete_user_conf(guild_id=ctx.guild.id, user_id=member.id, category=Botloader.Data.user_category['permission'], variable_key=variable)
            await ctx.reply(f"Membre {member} supprimé de la liste {variable} (valeur: {value})")
        except Exception as e:
            await ctx.reply(f"Erreur: {e}.")

    @commands.command(name="getdata")
    async def getdata(self, ctx: Context, member: discord.Member, variable):
        if not Botloader.owner_permission.check(ctx.author.id):
            return
        try:
            value = Botloader.Data.get_user_conf(guild_id=ctx.guild.id, user_id=member.id, category=Botloader.Data.user_category['permission'], variable_key=variable)
            await ctx.reply(f"Valeur de la variable {variable} pour {member}: {value}")
        except Exception as e:
            await ctx.reply(f"Erreur: {e}.")

    @commands.command(name="updateliste")
    async def updateliste(self, ctx: Context, member: discord.Member, variable, new_value):
        if not Botloader.owner_permission.check(ctx.author.id):
            return
        try:
            value = Botloader.Data.get_user_conf(guild_id=ctx.guild.id, user_id=member.id, category=Botloader.Data.user_category['permission'], variable_key=variable)
            Botloader.Data.update_user_conf(guild_id=ctx.guild.id, user_id=member.id, category=Botloader.Data.user_category['permission'], variable_key=variable, variable_value=new_value)
            await ctx.reply(f"Valeur de la variable {variable} pour {member} mise à jour: {value} => {new_value}.")
        except Exception as e:
            await ctx.reply(f"Erreur: {e}.")

    @commands.command(name="off")
    async def off(self, ctx: Context):
        if not Botloader.owner_permission.check(ctx.author.id):
            return
        await ctx.send("Bot was offline.")
        await asyncio.sleep(3)
        print("")
        Botloader.Bot.console("INFO", f'Bot Closed')
        print("")
        await self.bot.close()
        
    @commands.command(name="invits")
    async def invits(self, ctx: Context):
        if not Botloader.owner_permission.check(ctx.author.id):
            return
        for guild in self.bot.guilds:
            try:
                invite = await guild.text_channels[0].create_invite(max_uses=1, unique=True)
                await ctx.send(f'Invitation pour le serveur {guild.name}: {invite.url}')
            except discord.Forbidden:
                 print(f"Le bot n'a pas les permissions nécessaires pour créer une invitation dans le serveur {guild.name}")