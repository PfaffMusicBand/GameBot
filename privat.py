import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import Botloader
from typing import List
import os
from random import randint

class Privat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def voca_autocompletion(self, interaction: discord.Interaction,current: str) -> List[app_commands.Choice[str]]:
            langs = ['allemand','anglais', 'test']
            return [
                    app_commands.Choice(name=lang, value=lang)
                    for lang in langs if current.lower() in lang.lower()
                ]

    voca_user_data = {}
    ctx_mapping ={}
    
    @commands.hybrid_command(name = "voca")
    @app_commands.autocomplete(lang = voca_autocompletion)
    async def testvoca(self, interaction: Context, lang: str, nombre: int):
        await Privat.test_voca_logic(self.bot, interaction, lang, nombre)

    async def test_voca_logic(self, ctx: Context, lang, nombre):
        Privat.voca_user_data[ctx.author.id] = f"{lang}, {nombre}"
        q = {}
        r = {}
        mots = 0
        try:
            with open(f"{lang}.txt", "r", encoding="utf-8") as voca:
                entete = voca.readline()
                fr, lg = entete.strip().split(",")
                for ligne in voca:
                    if "'''" in ligne:
                        while "'''" not in ligne:
                            pass
                    else:
                        quest, trad = ligne.strip().split(",")
                        mots += 1
                        q[mots] = quest
                        r[mots] = trad
        except Exception as e:
            await ctx.reply("Une erreur s'est produite.", ephemeral=True)
            Botloader.Bot.console("WARN", e)
            return
        if mots == 0:
            await ctx.reply(f"Aucun mot trouvé dans le test de {lang}.", ephemeral=True)
        else:
            embed = discord.Embed(title = f"Teste de vocabulaire {lang}", description = f"{mots} mots ressancés", color=discord.Colour.blue())
            embed.set_thumbnail(url = "https://cdn3.emoji.gg/emojis/1041-zenitsu-yelena.png")
            if int(nombre) > mots:
                nombre = mots
                embed.add_field(name="**Erreur:**", value=f"**Le nombre de questions demandé est supèrieur au nombre de mots ressancés, vous n'aurez donc que {mots} questions.**", inline=False)
            embed.add_field(name = "Règles:", value =  
                    f"""
                        Bienvenue {ctx.author.mention} sur le teste de vocabulaire d'{lang}.
                        Vous avez demandez un test de **{nombre} mots**.

                        Nous alons vous demander une à une les traduction de {nombre} mots pris au hazard dans une base de donnée de {mots} mots, pour y répondre veuillez envoyer votre réponse dans ce channel.
                        Après chaque réponse un microbilant vous est fournie, à la fin de la séssion un bilan complet.
                        En cas d'écheque ou d'erreure de la comande veuillez contacter un administrateur.
                        La vérification ignore les articles mais prend en compte les majuscules.

                        **IMPORTANT! Les eszetts (ß) serrons remplassé par "ss"**.
                        """
                    , inline = True)
            await ctx.channel.send(embed=embed)
            j, f, total = 0, 0, 0
            faut = []
            checked = []
            for i in range(int(nombre)):
                nbr = randint(1, mots)
                while nbr in checked:
                    nbr = randint(1, mots)
                checked.append(nbr)
                question = q[nbr]
                reponse = r[nbr]
                total = total + 1
                embed = discord.Embed(title = "Quelle est la traduction de", description = f"**{question}**", color=discord.Colour.dark_theme())
                embed.set_footer(text = f"Question: {total}/{nombre}")
                await ctx.channel.send(embed=embed)
                def checkMessage(message):
                    return ctx.author == message.author and ctx.channel == message.channel
                rep = await self.wait_for("message", check = checkMessage)
                if rep.content in reponse:
                    j, titre, color, url = j + 1, "Juste", discord.Colour.green(), "https://cdn3.emoji.gg/emojis/2990_yes.png"
                else:
                    faut.append(nbr)
                    f, titre, color, url = f + 1, "Faux", discord.Colour.red(), "https://cdn3.emoji.gg/emojis/1465-x.png"
                reu = j * 100 /total
                embed = discord.Embed(title = titre, description = 
                            f"""
                            La réponse est **{reponse}**
                            {int(reu)}% de réussite.
                            """, color=color)
                embed.set_thumbnail(url = url)
                await ctx.channel.send(embed=embed)
                await ctx.channel.send(file=discord.File(Botloader.FFMPEG.maketts(reponse, lg, name=f"{reponse}.mp3")))
                os.remove(f'{reponse}.mp3')
            note = j*20/total
            note = round(note, 1)
            reu = round(reu, 2)
            embed = discord.Embed(title = "Résultats", description = f"**{note}/20**", color=discord.Colour.from_rgb(255, 255, 255))
            embed.set_thumbnail(url = "https://cdn3.emoji.gg/emojis/3323-guilty.png")
            embed.add_field(name = "Remarque", value = 
                    f"""
                    Bravos, vous avez finit le test de vocabulaire!
                    Vous avez répondu juste à **{j}/{total}** questions.
                    Votre note est de **{note}/20**, soit **{reu}%** de réussite.
                    """
                    , inline = True)
            await ctx.channel.send(embed=embed)
            if len(faut) != 0:
                embed = discord.Embed(title="Révision", description="Liste de mots à réviser.", color=discord.Colour.blue())
                value = ""
                for nbr in faut:
                    value = f"{value}\n**{r[nbr]}**:\n{q[nbr]}"
                embed.add_field(name=f":sweat:", value=value, inline=False)
                await ctx.channel.send(embed=embed)
        view = discord.ui.View()
        item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Relancer le test", custom_id="restart_test", disabled=False)
        view.add_item(item=item)
        Privat.ctx_mapping[ctx.author.id] = ctx
        await ctx.channel.send(view=view)
        return

    #spam commande
    @commands.hybrid_command(name="dm")
    async def dm(self, ctx: Context, mention: discord.User,*,msg):
        message = ctx.message
        if len(message.attachments) > 1:
            await ctx.reply("Vous ne pouvez envoyer qu'un seul fichier à la fois.")
            return
        try:
            channel = await mention.create_dm()
        except discord.Forbidden: ctx.reply("Impossible d'envoyer le message.")
        embed = discord.Embed(title = "**Message**", description = msg, color=discord.Colour.dark_magenta())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
        view = discord.ui.View()
        item = discord.ui.Button(style=discord.ButtonStyle.danger, label="Signaler un Spam", custom_id= "Spam", disabled=False)
        view.add_item(item=item)
        if message.attachments :
            embed.add_field(name="**Pièce(s) Jointe(s)**", value=f"Pièce joints envoyé par {ctx.author}.")
            for attachment in message.attachments:
                await attachment.save(Botloader.Downloader.get_path(attachment.filename))
                file=discord.File(Botloader.Downloader.get_path(attachment.filename))
                await channel.send(embed=embed ,view=view, file=file)
                os.remove(Botloader.Downloader.get_path(attachment.filename))
        else:
            await channel.send(embed=embed ,view=view)
        return
        
def setup(bot):
    bot.add_cog(Privat(bot))