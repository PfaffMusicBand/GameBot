import os
from gtts import gTTS
from Levenshtein import distance
from datetime import datetime
import inspect
import sqlite3
import pytz
from collections import defaultdict
import asyncio
import discord
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
class AutoMod:
    black_liste = []

    @staticmethod
    def check_word_init():
        with open("blackword.txt", "r", encoding="utf-8") as data:
            return [ligne.strip() for ligne in data]

    @staticmethod
    def var_word_init():
        variation = defaultdict(list)
        with open("blackwordvariation.txt", "r", encoding="utf-8") as data:
            for line in data:
                vars, true_var = line.strip().split("@")
                vars = vars.split(",")
                true_var = true_var.split(",")
                for var in vars:
                    variation[var].extend(true_var)
        return variation

    @staticmethod
    def preprocess_word(word):
        word = word.lower()
        remplacements = {
        'à': 'a', '@': 'a', 'â': 'a', 'ä': 'a',
        'ô': 'o', 'ö': 'o',
        'ç': 'c',
        'û': 'u', 'ü': 'u',
        'ê': 'e', 'ë': 'e',
        'î': 'i', 'ï': 'i'
    }
        translation_table = str.maketrans("", "", r",;.:!?/-+&\"#'{([-|`_)=}]°$£¤µ%§")
        word = word.translate(translation_table)
        translation_table = str.maketrans(remplacements)
        word = word.translate(translation_table)
        word = word.replace("\n", "")
        modified_word = ""
        count = 1
        for i in range(1, len(word)):
            if word[i] == word[i - 1]:
                count += 1
            else:
                if count >= 3:
                    modified_word += word[i - 1] * 2
                else:
                    modified_word += word[i - count:i]
                count = 1
        if count >= 3:
            modified_word += word[-1] * 2
        else:
            modified_word += word[-count:]
        return modified_word

    @staticmethod
    def check_from_dictionary(word):
        if word in map(str.lower, AutoMod.check_word_init()):
            return True, word, 1
        return False, "", 0
    
    @staticmethod
    def check_from_levenshtein(word):
        tword = min(AutoMod.check_word_init(), key=lambda bword: distance(bword, word) / len(bword))
        similarity = 1 - (distance(word, tword) / max(len(word), len(tword)))
        return tword, similarity
    
    @staticmethod
    def check_word(word):
        tword = ""
        similarity = 0
        processed_word = AutoMod.preprocess_word(word)
        if all(c.isalpha() or c.isspace() for c in processed_word):
            check, word, similarity = AutoMod.check_from_dictionary(processed_word)
            if check:
                return True, word, 1
            else:
                tword, similarity = AutoMod.check_from_levenshtein(processed_word)
                if similarity < 0.3:
                    return False, tword, similarity
                var_word = AutoMod.var_word_init()
                combinations = [processed_word]
                for key in var_word:
                    if key in processed_word:
                        new_combinations = []
                        for variation in var_word[key]:
                            for word in combinations:
                                new_word = AutoMod.preprocess_word(word.replace(key, variation))
                                if len(new_word) < 10 and new_word not in new_combinations:
                                    new_combinations.append(new_word)
                        for world in new_combinations:
                            combinations.append(world)
                if combinations != "":
                    for new_word in combinations:
                        a,similarity = AutoMod.check_from_levenshtein(processed_word)
                        check, _, c = AutoMod.check_from_dictionary(new_word)
                        if check:
                            return True, new_word, similarity
                return False, "", 0
        else:
            combinations = [processed_word]
            var_word = AutoMod.var_word_init()
            for key in var_word:
                if key in processed_word:
                    new_combinations = []
                    for variation in var_word[key]:
                        for word in combinations:
                            new_word = processed_word.replace(key, variation)
                            new_word = AutoMod.preprocess_word(new_word)
                            if len(new_word) < 16 and new_word not in new_combinations:
                                new_combinations.append(new_word)
                    combinations = new_combinations
            for new_word in combinations:
                tword, similarity = AutoMod.check_from_levenshtein(processed_word)
                if similarity > 0.70:
                    return True, tword, similarity
            return False, tword, similarity
    
    def check_message(message: str):
        black_word = {}
        black_word_similarity = {}
        message_content = message.split(" ")
        for word in message_content:
            check, true_word, similarity = AutoMod.check_word(word)
            if check:
                black_word[word] = true_word
                black_word_similarity[word] = similarity
        return black_word, black_word_similarity


import sqlite3

import sqlite3

import sqlite3

class Data:
    cmd_value = {
        'sayic': 'say_in_channel_permission',
        'say': 'say_command_permission',
        'dm': 'privat_message_bot_permission',
        'vtts': 'vtts_command_permission',
        'ftts': 'ftts_commande_permission',
        'rdm': 'rdm_commande_permission',
        'voca': 'voca_commande_permission',
        'vtts_l': 'vtts_direct_message_permission'
    }

    user_category = {
        'permission': 'permission_category',
        'xp': 'xp_category'
    }

    guild_conf = {
        'xp_message_by_character': 'xp_by_message_reward',
        'xp_vocal_by_minute': 'xp_by_vocal_reward'
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


    
class version:
    forward = [1.1, 1.2]
    recommanded = 1.3
    laster = 1.4

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
        await ctx.reply("L'intéraction a été expressément refusée car vous ne possédez pas les autorisations nécéssaire.")

    def maketts(text, langage="fr", name = "output.mp3"):
        tts_instance = gTTS(text, lang=langage)
        tts_instance.save(name)
        return name
    
    def check_level(message):
        level = Data.get_user_conf(message.guild.id, message.author.id, 'actual_xp_level')
        xp = Data.get_user_conf(message.guild.id, message.author.id, 'xp_reward_total')

    def console(type, arg):
        startTime = datetime.strftime(datetime.now(tz), '%H:%M:%S')
        print(f"[{startTime} {type}] {inspect.stack()[1].function}: {arg}")
    
    def Launched(launched_bot):
        launched_bot_class = globals()[launched_bot]
        Bot.Name = launched_bot_class.Name
        Bot.Token = launched_bot_class.__Token__
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

class BetaBelouga:
    Name= "BetaBelouga"
    __Token__ = "OTY5NTIwOTYyMjIxNTEwNjU2.Ymumwg.YXeEiL-gIwv_A_22t-mS2-jvVNQ"
    BotGuild = 969214672215625748
    AnnonceChannel = 1066680440209027152
    ConsoleChannel = 972036600357879828
    MessageChannel = 1009208789674754098
    BugreportChannel = 1239839087888830466
    Prefix = "BB"

class Belouga:
    Name= "Belouga"
    __Token__ = "OTcxNzUwMzU1NzY1NDM2NDI2.GWTHwA.FmvtUzb9M2DPNX3Pu6A4c4rcEjrnlNvj55uRPI"
    BotGuild = 969214672215625748
    AnnonceChannel = 1066680440209027152
    ConsoleChannel = 972036409085014046
    MessageChannel = 1175569633357598742
    BugreportChannel = 1239839087888830466
    Prefix = "BL"

class GameHub:
    Name = "GameHub"
    __Token__ = "MTEyNDA0NTEwNjU1MTQ1NTc1NA.GOpQbm.Q0XejDRLmgm4ipGXRDDbDxkcnKojgEqYNdOx5c"
    BotGuild = 1108421336042328125
    AnnonceChannel = 1141666570188361771
    ConsoleChannel = 1141666570188361771
    MessageChannel = 1141666570188361771
    BugreportChannel = 1141666570188361771
    VTTSListenerChannel = 1242185337053380738
    Prefix = "?"
    
