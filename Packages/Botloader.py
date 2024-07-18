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

class Data:
    cmd_value = {
        'sayic': 'say_in_channel_permission',
        'say': 'say_command_permission',
        'dm': 'privat_message_bot_permission',
        'vtts': 'vtts_command_permission',
        'ftts': 'ftts_commande_permission',
        'rdm': 'rdm_commande_permission',
        'voca': 'voca_commande_permission',
        'vtts_l': 'vtts_direct_message_permission',
        'execute': 'execute_command_permission',
        'blackliste_dm': 'blackliste_dm_member'
    }

    user_category = {
        'permission': 'permission_category',
        'xp': 'xp_category'
    }

    guild_conf = {
        'xp_message_by_character': 'xp_by_message_reward',
        'xp_vocal_by_minute': 'xp_by_vocal_reward',
        'automod_channel': 'automod_channel_report',
        'command_name': 'extra_command_name',
    }

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

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
    def insert_guild_conf(guild_id, conf_key, conf_value):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''INSERT OR REPLACE INTO guild_conf (guild_id, conf_key, conf_value)
                          VALUES (?, ?, ?)''', (guild_id, conf_key, conf_value))
        connection.commit()
        connection.close()

    @staticmethod
    def insert_user_conf(guild_id, user_id, conf_key, conf_value):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''INSERT OR REPLACE INTO user_conf (guild_id, user_id, conf_key, conf_value)
                          VALUES (?, ?, ?, ?)''', (guild_id, user_id, conf_key, conf_value))
        connection.commit()
        connection.close()

    @staticmethod
    def insert_user_game_data(user_id, guild_id, game_key, game_value):
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
    def update_guild_conf(guild_id, conf_key, conf_value):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''UPDATE guild_conf
                          SET conf_value = ?
                          WHERE guild_id = ? AND conf_key = ?''',
                       (conf_value, guild_id, conf_key))
        connection.commit()
        connection.close()

    @staticmethod
    def update_user_conf(guild_id, user_id, conf_key, conf_value):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''UPDATE user_conf
                          SET conf_value = ?
                          WHERE guild_id = ? AND user_id = ? AND conf_key = ?''',
                       (conf_value, guild_id, user_id, conf_key))
        connection.commit()
        connection.close()

    @staticmethod
    def update_user_game_data(user_id, guild_id, game_key, game_value):
        connection = sqlite3.connect(f"{Bot.Name}.db")
        cursor = connection.cursor()
        cursor.execute('''UPDATE user_game_data
                          SET game_value = ?
                          WHERE user_id = ? AND guild_id = ? AND game_key = ?''',
                       (game_value, user_id, guild_id, game_key))
        connection.commit()
        connection.close()

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
        startTime = datetime.strftime(datetime.now(tz), '%H:%M:%S')
        print(f"[{startTime} {type}] {inspect.stack()[1].function}: {arg}")

    def get_token(token, key):
        codes = token.split()
        token = ""
        for i, code in enumerate(codes):
            decalage = ord(key[i % len(key)])
            char = chr((int(code) - decalage)%256)
            token += char
        return token
    
    def Launched(launched_bot, pasword):
        launched_bot_class = globals()[launched_bot]
        Bot.Pasword = pasword
        Bot.Name = launched_bot_class.Name
        Bot.Token = Bot.get_token(launched_bot_class.__Token__, pasword)
        Bot.BotGuild = launched_bot_class.BotGuild
        Bot.AnnonceChannel = launched_bot_class.AnnonceChannel
        Bot.ConsoleChannel = launched_bot_class.ConsoleChannel
        Bot.MessageChannel = launched_bot_class.MessageChannel
        Bot.BugReportChannel = launched_bot_class.BugreportChannel
        Bot.Prefix = launched_bot_class.Prefix
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

class BetaBelouga:
    Name= "BetaBelouga"
    __Token__ = "145 185 205 150 144 185 189 216 145 185 205 218 143 207 189 217 144 185 185 216 144 207 201 147 112 190 225 214 175 220 219 143 155 189 217 166 171 177 161 200 139 220 234 192 131 196 166 147 182 146 225 180 116 146 222 215 152 179 197"
    BotGuild = 969214672215625748
    AnnonceChannel = 1066680440209027152
    ConsoleChannel = 972036600357879828
    MessageChannel = 1009208789674754098
    BugreportChannel = 1239839087888830466
    Prefix = "BB"

class Belouga:
    Name= "Belouga"
    __Token__ = "159 181 202 231 178 227 182 199 174 225 196 149 183 219 169 146 181 179 177 155 175 148 170 153 157 171 192 181 152 216 168 157 170 214 215 196 182 225 209 157 182 147 148 177 181 199 151 185 214 134 162 155 210 152 219 196 149 203 217 221 208 183 215 186 150 156 228 182 185 170"
    BotGuild = 969214672215625748
    AnnonceChannel = 1066680440209027152
    ConsoleChannel = 972036409085014046
    MessageChannel = 1175569633357598742
    BugreportChannel = 1239839087888830466
    Prefix = "$"

class GameHub:
    Name = "GameHub"
    __Token__ = "157 181 172 232 178 173 162 128 175 187 180 219 183 203 165 146 180 195 181 154 175 164 196 152 189 165 151 168 159 209 184 209 209 151 178 128 185 204 217 168 187 173 189 200 212 163 205 217 168 168 179 171 179 198 173 217 187 196 213 186 211 211 200 149 210 192 189 200 184 217 133 196"
    BotGuild = 1108421336042328125
    AnnonceChannel = 1141666570188361771
    ConsoleChannel = 1141666570188361771
    MessageChannel = 1141666570188361771
    BugreportChannel = 1141666570188361771
    VTTSListenerChannel = 1242185337053380738
    Prefix = "?"
    
