import discord
import asyncio
import os
from random import randint
from typing import Any
from discord.ext import commands
from datetime import datetime
from gtts import gTTS
import Botloader
import argparse
from  discord import app_commands
from typing import List

def main():
    parser = argparse.ArgumentParser(description='Scripte Bot V1.2')
    parser.add_argument('Botname', type=str, default="Bot", help='Nom du bot à lancer')
    args = parser.parse_args()
    Botloader.Bot.Launched(args.Botname)

if __name__ == '__main__':
    main()

# AIzaSyDc_KDH702AiUaJGZgapvPnydA0IWue0R0 tenor api key

statutpresence = ["you!", "cooked you!"]
botversion = 1.3 #version du scripte
r= "n"#ne pas modifier
command_descriptions = {}
#Bot
def init(bot):
    Botloader.Bot.Launched(bot)
bot = client = commands.Bot(command_prefix = Botloader.Bot.Prefix,intents=discord.Intents.all(),description = "Belouga.exe is watching you!!!")
bot.remove_command('help')

def console(type, arg):
    startTime = datetime.strftime(datetime.now(), '%H:%M:%S')
    print(f"[{startTime} {type}] {arg}")

#start events
@bot.event
async def on_ready():
    console("INFO", f'Logged in as {bot.user} (ID: {bot.user.id})')
    await versions(type = "on_ready", ctx = Any)
    await bot.change_presence(status = discord.Status.online,activity = discord.Game("Chargement des cookis!"))
    try:
        synced = await bot.tree.sync()
        console("INFO", f'Synced {len(synced)} commands')
    except Exception as e:
        console("WARN", f'Error: {e}')
    statut = randint(0,1)
    if statut == 1:
        actype = discord.ActivityType.playing
    else : actype = discord.ActivityType.watching
    statut = statutpresence[statut]
    await bot.change_presence(activity=discord.Activity(type = actype, name = statut))
    for command in bot.commands:
        if command.help:
            command_descriptions[command.name] = command.help
    print("")
    while True:
        h, m, s = datetime.strftime(datetime.now(), '%H'), datetime.strftime(datetime.now(), '%M'), datetime.strftime(datetime.now(), '%S')
        if h == m:
            if h == s:
                guild = bot.get_guild(Botloader.Bot.BotGuild)
                channel = guild.get_channel_or_thread(Botloader.Bot.AnnonceChannel)
                ping = await channel.send(f"@here il est {h}h{m}")
                await ping.publish()
                await asyncio.sleep(60-(int(s)-1))
                ping = await channel.send("Trop tard!")
                await ping.publish()
        await asyncio.sleep(1)

#versions fonction
async def versions(type, ctx):
    if botversion == float(Botloader.version.recommanded):
        description, color, url = "Votre bot est à jour.", discord.Colour.green(), "https://cdn3.emoji.gg/emojis/2990_yes.png"
    elif botversion < float(Botloader.version.recommanded):
        description, color, url = "Attention : votre bot n'est plus à jour !", discord.Colour.from_rgb(250, 0, 0), "https://cdn3.emoji.gg/emojis/1465-x.png"
    else: description, color, url = "Attention : votre bot est en version bêta !", discord.Colour.orange(), "https://cdn3.emoji.gg/emojis/3235_warning2.png"
    if type == "commande":
        embed = discord.Embed(title="Notes de mise à jour", description=description, color=color)
        embed.set_thumbnail(url=url)
        embed.add_field(name="Version du bot :", value=botversion, inline=False)
        embed.add_field(name="Version recommandée :", value=Botloader.version.recommanded, inline=False)
        embed.add_field(name="Dernière version :", value=Botloader.version.recommanded, inline=False)
        await ctx.channel.send(embed=embed)
    if type == "on_ready":
        console("INFO", f'Logged in V{botversion}')

# Commande help
@bot.command(help = f"Aide pour les commandes du bot.\nSyntaxe: `{Botloader.Bot.Prefix}help <commande(optionnel)>`")
async def help(ctx, *args):
    if not args:
        # Afficher la liste des commandes et leurs descriptions
        embed = discord.Embed(title="Liste des commandes disponibles:", description="Certaine commandes ne sont pas ressancées ici.", color=discord.colour.Colour.brand_green())
        for command, description in command_descriptions.items():
            embed.add_field(name=f"{Botloader.Bot.Prefix}{command}", value=description, inline=False)
        await ctx.send(embed = embed)
    else:
        # Afficher la description spécifique d'une commande
        command_name = args[0]
        description = command_descriptions.get(command_name, "Aucune description disponible.")
        embed = discord.Embed(title=f"{Botloader.Bot.Prefix}{command_name}", description=description, color=discord.colour.Colour.brand_green())
        await ctx.send(embed = embed)

#ping
@bot.command(help = "Ping du bot.")
async def ping(ctx):
    embed=discord.Embed(title="PONG", description=f":ping_pong: Le ping est de **{round(client.latency)}** secondes!")
    await ctx.send(embed=embed)

#say commande
@bot.command()
async def sayInChannel(ctx, channel : discord.TextChannel, text):
    await channel.send(text)
    MTD2 = await ctx.channel.send(f"Votre message a bien été envoyé dans #{channel}!")
    MTD1 = ctx.message
    await asyncio.sleep(4)
    await MTD1.delete()
    await MTD2.delete()

@bot.command(help = f"Faire parler le bot.\nSyntaxe: `{Botloader.Bot.Prefix}say <argument>`")
async def say(ctx,*, text):
    messagetodelete = ctx.message
    await messagetodelete.delete()
    await ctx.send(text)
    channel= ctx.channel

#clear msg in curant channel
@bot.command(help = f"Suprimé les n dernier messages dans le channel.\nSyntaxe: `{Botloader.Bot.Prefix}clear <argument(int)>`")
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount):
    try:
        await ctx.channel.purge(limit= int(amount))
    except: # Error handler
        await ctx.send('Please enter a valid integer as amount.')

#afficher un avatar
@bot.command(help = f"Afficher l'avatar d'un membre.\nSyntaxe: `{Botloader.Bot.Prefix}avatar <discord.Member>`")
async def avatar(ctx, member:discord.Member):
	try : 
		embed = discord.Embed(title = f"Voici l'avatar de {member} :",color = discord.Colour.blue())
		embed.set_image(url = member.avatar)
		await ctx.send(embed=embed)
		await ctx.message.delete()
	except Exception as errors:
		await ctx.send(embed= discord.Embed(title = ":x: Une erreur a eu lieu.", description = f"L'erreur est la suivante : `{errors}`."))

@bot.tree.command(name = "randome")
async def randome(interaction: discord.Interaction, min: int, max: int):
    try:
        if int(max) > int(min):
            num = randint(int(min), int(max))
        else:
            num = randint(int(max), int(min))
        embed = discord.Embed(title="Random", description=f"Voici un nombre aléatoire entre {min} et {max}")
        embed.set_thumbnail(url="https://media.tenor.com/IfbgWLbg_88AAAAC/dice.gif")
        embed.add_field(name="Nombre:", value=num, inline=False)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Erreur : {e}")


#slash command voca

async def voca_autocompletion(
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        langs = ['anglais', 'test', 'allemand']
        return [
                app_commands.Choice(name=lang, value=lang)
                for lang in langs if current.lower() in lang.lower()
            ]

voca_user_data = {}
@bot.tree.command(name="voca")
@app_commands.autocomplete(lang = voca_autocompletion)
async def testvoca(interaction: discord.Interaction, lang: str, nombre: int):
    await test_voca_logic(interaction, lang, nombre)

async def test_voca_logic(interaction: discord.Interaction, lang, nombre):
    voca_user_data[interaction.user.id] = f"{lang}, {nombre}"
    q = {}
    r = {}
    mots = 0
    try:
        with open(f"{lang}.txt", "r", encoding="utf-8") as voca:
            entete = voca.readline()
            fr, lg = entete.strip().split(",")
            for ligne in voca:
                quest, trad = ligne.strip().split(",")
                mots += 1
                q[mots] = quest
                r[mots] = trad
    except Exception as e:
        await interaction.response.send_message("Une erreur s'est produite.", ephemeral=True)
        print(f"An unexpected error occurred: {e}")
        return
    if mots == 0:
        await interaction.response.send_message(f"Aucun mot trouvé dans le test de {lang}.", ephemeral=True)
    else:
        embed = discord.Embed(title = f"Teste de vocabulaire {lang}", description = f"{mots} mots ressancés", color=discord.Colour.blue())
        embed.set_thumbnail(url = "https://cdn3.emoji.gg/emojis/1041-zenitsu-yelena.png")
        if int(nombre) > mots:
            nombre = mots
            embed.add_field(name="**Erreur:**", value=f"**Le nombre de questions demandé est supèrieur au nombre de mots ressancés, vous n'aurez donc que {mots} questions.**", inline=False)
        embed.add_field(name = "Règeles:", value =  
                f"""
                    Bienvenue {interaction.user.mention} sur le teste de vocabulaire d'{lang}.
                    Vous avez demandez un test de **{nombre} mots**.

                    Nous alons vous demander une à une les traduction de {nombre} mots pris au hazard dans une base de donnée de {mots} mots, pour y répondre veuillez envoyer votre réponse dans ce channel.
                    Après chaque réponse un microbilant vous est fournie, à la fin de la séssion d'entrainement un bilan complet vous serra remit.
                    En cas d'écheque ou d'erreure de la comande veuillez contacter un administrateur.
                    La vérification ignore les articles mais prend en compte les majuscules.

                    **IMPORTANT! Les eszetts (ß) serrons remplassé par "ss"**.
                    """
                , inline = True)
        await interaction.response.send_message(embed=embed)
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
            await interaction.channel.send(embed=embed)
            def checkMessage(message):
                return interaction.user == message.author and interaction.channel == message.channel
            rep = await bot.wait_for("message", check = checkMessage)
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
            await interaction.channel.send(embed=embed)
            await interaction.channel.send(file=discord.File(Botloader.maketts(reponse, lg, name=f"{reponse}.mp3")))
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
        await interaction.channel.send(embed=embed)
        if len(faut) != 0:
            embed = discord.Embed(title="Révision", description="Liste de mots à réviser.", color=discord.Colour.blue())
            value = ""
            for nbr in faut:
                value = f"{value}\n**{r[nbr]}**:\n{q[nbr]}"
            embed.add_field(name=f":sweat:", value=value, inline=False)
            await interaction.channel.send(embed=embed)
    view = discord.ui.View()
    item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Relancer le test", custom_id="restart_test", disabled=False)
    view.add_item(item=item)
    await interaction.channel.send(view=view)
    return

#spam commande
@bot.command()
async def dm(ctx , mention: discord.User,*,msg):
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
    await message.delete()
    
#vocal command

#vocal command
@bot.command()
async def join(ctx):
    if ctx.voice_client is not None:
        await ctx.send("Le bot est déjà connecté à un canal vocal.")
        return
    if ctx.author.voice is None:
        await ctx.send("Vous devez être dans un canal vocal pour utiliser cette commande.")
        return
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send("Le bot n'est pas connecté à un canal vocal.")
        return
    await ctx.voice_client.disconnect()
    
@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()

blackliste = [388026287941484544,423500858756694016]
@bot.command(help  = f"Faire parler le bot dans le salon vocale (existe en slash commande sans chois de langue).\nSyntaxe:`{Botloader.Bot.Prefix}vtts <langage(ex: fr)> <text>`")
async def vtts(ctx,lg, *, text_to_speak):
    if ctx.voice_client is None:
        await ctx.send("Le bot n'est pas connecté à un canal vocal. Utilisez !join pour le faire rejoindre un canal vocal.")
        return
    if ctx.author.id in blackliste:
        return ctx.send("vas te laver")
    tts = gTTS(text=text_to_speak, lang=lg)
    tts.save('output.mp3')
    ctx.voice_client.play(discord.FFmpegPCMAudio(executable=Botloader.FFMPEG.executable, source='output.mp3'))
    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)
    os.remove('output.mp3')

blackliste = [831971146386636820,388026287941484544,852926734860943403]

@bot.tree.command(name = "vtts")
async def slashvtts(interaction: discord.Interaction, tts: str):
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

@bot.command(help = f"Génère un mp3 à partire d'un message.\nSyntaxe: `{Botloader.Bot.Prefix}tts <langage(ex: fr)> <text>`")
async def tts(ctx,lg, *, text_to_speak):
    tts = gTTS(text=text_to_speak, lang=lg)
    tts.save('output.mp3')
    with open('output.mp3', 'rb') as f:
        await ctx.send(file=discord.File(f, filename='output.mp3'))
    os.remove('output.mp3')

#commandes sensibles
'''
Les commandes suivante sont réservé au déveloper pour des action de debugage.
'''
#version commande pas compltm privé
@bot.command(help = "Information sur la version du scripte.")
async def version(ctx):
    await versions(type="commande", ctx=ctx)
    
#shutdown commande
@bot.command()
async def off(ctx):
    if Botloader.owner_permission.check(ctx.author.id) != True:
        return await ctx.reply("Vous ne disposez pas des autorisations nécéssaire.")
    await ctx.send("Bot was offline.")
    asyncio.sleep(3)
    print("")
    console("INFO", f'Bot Closed')
    print("")
    await bot.close()

@bot.command()
async def restart(ctx):
    if Botloader.owner_permission.check(ctx.author.id) != True:
        return await ctx.reply("Vous ne disposez pas des autorisations nécéssaire.")
    await ctx.send("Bot was offline for restart.")
    await asyncio.sleep(3)
    print("")
    console("INFO", f'Bot Closed for restart')
    print("")
    global r
    r = "y"
    await bot.close()
    
#usles
@bot.command()
async def invits(ctx):
    if Botloader.owner_permission.check(ctx.author.id) != True:
        return
    for guild in bot.guilds:
        try:
            invite = await guild.text_channels[0].create_invite(max_uses=1, unique=True)
            await ctx.send(f'Invitation pour le serveur {guild.name}: {invite.url}')
        except discord.Forbidden:
             print(f"Le bot n'a pas les permissions nécessaires pour créer une invitation dans le serveur {guild.name}")

#button event
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "restart_test":
            view = discord.ui.View()
            item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Relancer le test", custom_id="restart_test", disabled=True)
            view.add_item(item=item)
            await interaction.channel.last_message.edit(view=view)
            lang, nombre = voca_user_data.get(interaction.user.id, "").split(",")
            await test_voca_logic(interaction, lang, nombre)
        if interaction.data["custom_id"] == "Spam":
            view = discord.ui.View()
            item = discord.ui.Button(style=discord.ButtonStyle.danger, label="Signaler un Spam", custom_id="dm_spam", disabled=True)
            view.add_item(item=item)
            await interaction.message.edit(view=view)
            embed = discord.Embed(title = "**Signalement**", description = f"Le message a bien été signalé.", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed)

#cheking messages
@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id or message is discord.Interaction:
        pass
    else:
        blw, blws = Botloader.auto_mod.check_message(message.content)
        if len(blw) != 0:
            guild = bot.get_guild(Botloader.Bot.BotGuild)
            channel = guild.get_channel(Botloader.Bot.MessageChannel)
            startTime = datetime.strftime(datetime.now(), '%H:%M:%S')
            if isinstance(message.channel, discord.channel.DMChannel):
                zone = "DM"
            else:
                zone = "Serveur"
            embed = discord.Embed(title = zone, description = startTime, color=discord.Color.brand_red())
            embed.set_thumbnail(url = message.author.avatar)
            embed.add_field(name = "User:", value = message.author.mention, inline = False)
            embed.add_field(name = "Server:", value = message.guild, inline = False)
            embed.add_field(name = "Channel:", value = f"<#{message.channel.id}>", inline = False)
            embed.add_field(name = F"Message:", value = f"[{message.content}]({message.jump_url})", inline = False)
            for key in blw:embed.add_field(name=f"Mot {key} détecté:", value=f"{round(blws[key], 2)*100}% de resemblance avec **{blw[key]}**.", inline=False)
            if message.attachments:
                for attachment in message.attachments:
                    embed.add_field(name="Attachment", value= attachment.proxy_url, inline=False)
            await channel.send(embed=embed)
    await client.process_commands(message)

bot.run(Botloader.Bot.Token)

os.system(f"python Launcher.py --bot {Botloader.Bot.Name} --version {botversion} --restart {r}")