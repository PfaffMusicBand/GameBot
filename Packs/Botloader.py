"""
Module Botloader
----------------
Regroupe tous les éléments essentiels

Le module permet de récupérer toutes les variables essentielles au bot ainsi que les données des guildes et des utilisateurs.

Data
-----
`Data`

Bot
----
`Bot`
>>> Bot.Name
>>> Bot.Token
>>> Bot.Prefix
"""
import os
import math
import asyncio
import discord
import inspect
import sqlite3
import pytz
import sqlite3
from gtts import gTTS
from datetime import datetime
from collections import deque
from enum import Enum


__path__ = os.path.dirname(os.path.abspath(__file__))
tz = pytz.timezone('Europe/Paris')
    
class Downloader:
    download_path = r"download"
    def get_path(name):
        file_path = f"{Downloader.download_path}\\{name}"
        return file_path
          
class owner_permission:

    owner_id  = 592737249481850896

    def check(member_id):
        if member_id != owner_permission.owner_id:
            return False
        else: return True

class Conf():

    config_vars = {}

    with open(".conf", "r") as config_file:
        for line in config_file:
            if line.strip() and not line.startswith("#"):
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                config_vars[key] = value

class Data:
    """
    Data
    -----
    Module Database

    Fonctionnalités
    ----------------
    Pour récupérer une valeur:
    - Guild : `Data.get_guild_conf`
    - Utilisateur de guild : `Data.get_user_conf`

    Pour insérer / modifier:
    - Guild : `Data.set_guild_conf`
    - Utilisateur de guild : `Data.set_user_conf`

    Pour supprimer:
    - Guild : `Data.delete_guild_conf`
    - Utilisateur : `Data.delete_user_conf`

    Tips
    -----
    Pour récupérer plus facilement une clé de Database : `Data.<NOM_DE_CLEF>`

    Exemple
    --------
    >>> Data.CUSTOM_COMMANDS_NAMES
    >>> Data.get_guild_conf(guild_id, Data.AUTOMOD_CHANNEL)
    >>> Data.set_guild_conf(guild_id, Data.AUTOMOD_CHANNEL, value)
    >>> Data.delete_guild_conf(guild_id, Data.AUTOMOD_CHANNEL)
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    key_value = key = {
        'execute':'command_execute_permission',
        'custom_commands_names':'custom_commands_names',
        'sayic':'command_sayic_permission',
        'say':'command_say_permission',
        'vtts':'command_vtts_permission',
        'ftts':'command_ftts_permission',
        'randome':'command_rdm_permission',
        'testvoca':'command_testvoca_permission',
        'dm':'command_dm_permission',
        'dm_blackliste':'blackliste_dm_id',
        'automod_channel':'automod_channel_id',
        'automod_level': 'automod_action_level',
        'vtts_directe_message':'vtts_directe_message'

    }

    keys = list(key_value.keys())

    EXECUTE = keys[0]
    CUSTOM_COMMANDS_NAMES = keys[1]
    SAYIC = keys[2]
    SAY = keys[3]
    VTTS = keys[4]
    FTTS = keys[5]
    RANDOM = keys[6]
    TESTVOCA = keys[7]
    DM = keys[8]
    DM_BLACKLISTE = keys[9]
    AUTOMOD_CHANNEL = keys[10]
    AUTOMOD_LEVEL = keys[11]
    VTTS_DIRECTE_MESSAGE = keys[12]

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS guild_conf (
                                guild_id INTEGER,
                                conf_key TEXT,
                                conf_value TEXT,
                                PRIMARY KEY (guild_id, conf_key)
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_conf (
                                guild_id INTEGER,
                                user_id INTEGER,
                                conf_key TEXT,
                                conf_value TEXT,
                                PRIMARY KEY (guild_id, user_id, conf_key)
                            )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_game_data (
                                user_id INTEGER,
                                guild_id INTEGER,
                                game_key TEXT,
                                game_value TEXT,
                                PRIMARY KEY (user_id, guild_id, game_key)
                            )''')

        # Ajout des index pour améliorer les performances des requêtes
        self.cursor.execute('''CREATE INDEX IF NOT EXISTS idx_guild_conf ON guild_conf (guild_id, conf_key)''')
        self.cursor.execute('''CREATE INDEX IF NOT EXISTS idx_user_conf ON user_conf (guild_id, user_id, conf_key)''')
        self.cursor.execute('''CREATE INDEX IF NOT EXISTS idx_user_game_data ON user_game_data (user_id, guild_id, game_key)''')

        self.connection.commit()

    @staticmethod
    def set_guild_conf(guild_id, conf_key, conf_value):
        data =  Data.get_guild_conf(guild_id, conf_key)
        if data:
            connection = sqlite3.connect(f"{Bot.Name}.db")
            cursor = connection.cursor()
            cursor.execute('''UPDATE guild_conf
                            SET conf_value = ?
                            WHERE guild_id = ? AND conf_key = ?''',
                        (conf_value, guild_id, conf_key))
            connection.commit()
            connection.close()
        else:
            connection = sqlite3.connect(f"{Bot.Name}.db")
            cursor = connection.cursor()
            cursor.execute('''INSERT OR REPLACE INTO guild_conf (guild_id, conf_key, conf_value)
                            VALUES (?, ?, ?)''', (guild_id, conf_key, conf_value))
            connection.commit()
            connection.close()

    @staticmethod
    def set_user_conf(guild_id, user_id, conf_key, conf_value):
        data =  Data.get_user_conf(guild_id, user_id, conf_key)
        if data:
            connection = sqlite3.connect(f"{Bot.Name}.db")
            cursor = connection.cursor()
            cursor.execute('''UPDATE user_conf
                            SET conf_value = ?
                            WHERE guild_id = ? AND user_id = ? AND conf_key = ?''',
                        (conf_value, guild_id, user_id, conf_key))
            connection.commit()
            connection.close()
        else:
            connection = sqlite3.connect(f"{Bot.Name}.db")
            cursor = connection.cursor()
            cursor.execute('''INSERT OR REPLACE INTO user_conf (guild_id, user_id, conf_key, conf_value)
                            VALUES (?, ?, ?, ?)''', (guild_id, user_id, conf_key, conf_value))
            connection.commit()
            connection.close()

    @staticmethod
    def set_user_game_data(user_id, guild_id, game_key, game_value):
        data = Data.get_user_game_data(user_id, guild_id, game_key)
        if data:
            connection = sqlite3.connect(f"{Bot.Name}.db")
            cursor = connection.cursor()
            cursor.execute('''UPDATE user_game_data
                            SET game_value = ?
                            WHERE user_id = ? AND guild_id = ? AND game_key = ?''',
                        (game_value, user_id, guild_id, game_key))
            connection.commit()
            connection.close()
        else:
            connection = sqlite3.connect(f"{Bot.Name}.db")
            cursor = connection.cursor()
            cursor.execute('''INSERT OR REPLACE INTO user_game_data (user_id, guild_id, game_key, game_value)
                            VALUES (?, ?, ?, ?)''', (user_id, guild_id, game_key, game_value))
            connection.commit()
            connection.close()

    @staticmethod
    def get_guild_conf(guild_id, conf_key):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''SELECT conf_value FROM guild_conf
                          WHERE guild_id = ? AND conf_key = ?''', (guild_id, conf_key))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def get_user_conf(guild_id, user_id, conf_key):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''SELECT conf_value FROM user_conf
                          WHERE guild_id = ? AND user_id = ? AND conf_key = ?''',
                       (guild_id, user_id, conf_key))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def get_user_game_data(user_id, guild_id, game_key):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''SELECT game_value FROM user_game_data
                          WHERE user_id = ? AND guild_id = ? AND game_key = ?''', (user_id, guild_id, game_key))
        result = cursor.fetchone()
        connection.close()
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def delete_guild_conf(guild_id, conf_key):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM guild_conf
                          WHERE guild_id = ? AND conf_key = ?''',
                       (guild_id, conf_key))
        connection.commit()
        connection.close()

    @staticmethod
    def delete_user_conf(guild_id, user_id, conf_key):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM user_conf
                          WHERE guild_id = ? AND user_id = ? AND conf_key = ?''',
                       (guild_id, user_id, conf_key))
        connection.commit()
        connection.close()

    @staticmethod
    def delete_user_game_data(user_id, guild_id, game_key):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM user_game_data
                          WHERE user_id = ? AND guild_id = ? AND game_key = ?''',
                       (user_id, guild_id, game_key))
        connection.commit()
        connection.close()

class Bot():
    """
    Bot
    ----

    Variables et fonctions essentielles pour le bot.

    Variables
    ----------

    Permet de réccupérer des info sur le Bot
    
    `Name` -> str()
    `Token` -> str()
    `BotGuild` -> int()
    `AnnonceChannel` -> int()
    `ConsoleChannel` -> int()
    `MessageChannel` -> int()
    `BugReportChannel` -> int()
    `Prefix` -> str()
    `Pasword` -> str()

    Fonctions
    ----------

    >>> `console` -> (voir Bot.console)
    >>> `maketts(text, langage, name = "output.mp3")` -> Retourne le nom d'un mp3 du texte fournit dans la langue fournit

    """

    queue = deque()

    async def play_audio(ctx, file):
        if ctx.voice_client.is_playing():
            Bot.queue.append((ctx, file))
            await ctx.reply("Audio ajouté à la file d'attente.", ephemeral=True)
        else:
            ctx.voice_client.play(discord.FFmpegPCMAudio(file), after=lambda e: Bot.on_play_finish(ctx, file))

    def on_play_finish(ctx, file):
        os.remove(file)
        if Bot.queue:
            next_ctx, next_file = Bot.queue.popleft()
            asyncio.run_coroutine_threadsafe(Bot.play_audio(next_ctx, next_file), ctx.bot.loop)

    async def on_refus_interaction(ctx, *arg):
        await ctx.reply("L'intéraction a été expressément refusée car vous ne possédez pas les autorisations nécéssaire.", ephemeral = True)

    def maketts(text, langage="fr", name = "output.mp3"):
        tts_instance = gTTS(text, lang=langage)
        tts_instance.save(name)
        return name
    
    async def check_level(message: discord.Message):
        print('1')
        level = int(Data.get_user_conf(message.guild.id, message.author.id, 'actual_xp_level'))
        xp = int(Data.get_user_conf(message.guild.id, message.author.id, 'xp_reward_total'))
        a = 64
        b = 100
        c = -154 - xp
        discriminant = b**2 - 4*a*c     
        sqrt_discriminant = math.sqrt(discriminant)
        x1 = (-b + sqrt_discriminant) / (2 * a)
        if x1 -1 < level:
            return
        else:
            new_level = level + 1
            if new_level > level:
                Data.update_user_conf(message.guild.id, message.author.id, 'actual_xp_level', new_level)
                await message.reply(f"Félicitations, vous gagnez un niveau (niveau {new_level})!")

    def console(type, arg):
        """
        Utilisation:
        ------------
        `type`: type de log (info, warn, error, debug)
        `arg`: se qui doit être print

        Exemple:
        --------
        >>> console("INFO", "Bot loggin")
        """
        colors = {
            "INFO": "\033[94m",  # Blue
            "WARN": "\033[93m",  # Yellow
            "ERROR": "\033[91m",  # Red
            "DEBUG": "\033[92m",  # Green
            "FUNCTION": "\033[35m",  # Violet
            "GRAY": "\033[90m",  # Gray
            "ENDC": "\033[0m"  # Reset color
        }
        now = datetime.now(tz)
        startDate = now.strftime('%Y-%m-%d')
        startTime = now.strftime('%H:%M:%S')
        color = colors.get(type.upper(), colors["ENDC"])
        print(f"{colors['GRAY']}{startDate} {startTime} {color}{type}{colors['ENDC']} {colors['FUNCTION']}{inspect.stack()[1].function}{colors['ENDC']}: {arg}")



    def get_token(token, key):
        codes = token.split()
        token = ""
        for i, code in enumerate(codes):
            decalage = ord(key[i % len(key)])
            char = chr((int(code) - decalage)%256)
            token += char
        return token
    
    def Launched(launched_bot, pasword):
        Bot.Pasword = pasword
        Bot.Name = Conf.config_vars.get(f"{launched_bot}_name")
        Bot.Token = Conf.config_vars.get(f"{launched_bot}_token")
        Bot.BotGuild = Conf.config_vars.get(f"{launched_bot}_guild")
        Bot.AnnonceChannel = Conf.config_vars.get(f"{launched_bot}_annonce_channel")
        Bot.ConsoleChannel = Conf.config_vars.get(f"{launched_bot}_console_channel")
        Bot.MessageChannel = Conf.config_vars.get(f"{launched_bot}_message_channel")
        Bot.BugReportChannel = Conf.config_vars.get(f"{launched_bot}_bugreport_channel")
        Bot.Prefix = Conf.config_vars.get(f"{launched_bot}_prefix")
        Bot.Database = Data(f"{Bot.Name}.db")

    Name = str()
    Token = str()
    BotGuild = int()
    AnnonceChannel = int()
    ConsoleChannel = int()
    MessageChannel = int()
    BugReportChannel = int()
    Prefix = str()
    Pasword = str()

class Reposit():
        
    repo_owner = Conf.config_vars.get("repo_owner")
    repo_name = Conf.config_vars.get("repo_name")
    token = Conf.config_vars.get("git_token")
