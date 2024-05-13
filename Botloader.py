import os
from gtts import gTTS
from Levenshtein import distance
from datetime import datetime
import inspect
__path__ = os.path.dirname(os.path.abspath(__file__))

class FFMPEG:
    executable = r"ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
    
    def maketts(text, langage="fr", name = "output.mp3"):
        tts_instance = gTTS(text, lang=langage)
        tts_instance.save(name)
        return name
    
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

class auto_mod:
    black_liste = []

    @staticmethod
    def check_word_init():
        with open("blackword.txt", "r", encoding="utf-8") as data:
            return [ligne.strip() for ligne in data]

    @staticmethod
    def var_word_init():
        variation = {}
        with open("blackwordvariation.txt", "r", encoding="utf-8") as data:
            for ligne in data:
                ligne = ligne.split(",")
                if ligne:
                    variation.update({var: ligne for var in ligne})
        return variation

    @staticmethod
    def preprocess_word(word):
        word = word.lower()
        translation_table = str.maketrans("", "", r",;.:!?/-+&\"#'{([-|`_)=}]°$£¤µ%§")
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
        if word in map(str.lower, auto_mod.check_word_init()):
            return True, word, 1
        return False, "", 0
    
    @staticmethod
    def check_from_levenshtein(word):
        tword = min(auto_mod.check_word_init(), key=lambda bword: distance(bword, word) / len(bword))
        similarity = 1 - (distance(word, tword) / max(len(word), len(tword)))
        return tword, similarity
    
    @staticmethod
    def check_word(word):
        processed_word = auto_mod.preprocess_word(word)
        if all(c.isalpha() or c.isspace() for c in processed_word):
            check, word, similarity = auto_mod.check_from_dictionary(processed_word)
            if check:
                return True, word, 1
            else:
                tword, similarity = auto_mod.check_from_levenshtein(processed_word)
                if similarity < 0.3:
                    return False, tword, similarity
                combinations = [processed_word]
                for key in auto_mod.var_word_init():
                    if key in processed_word:
                        new_combinations = []
                        for variation in auto_mod.var_word_init()[key]:
                            for word in combinations:
                                new_word = auto_mod.preprocess_word(word.replace(key, variation))
                                if len(new_word) < 10 and new_word not in new_combinations:
                                    new_combinations.append(new_word)
                        combinations = new_combinations
                    counter = 0
                for word in combinations:
                    counter = counter+1
                for new_word in combinations:
                    check, _, similarity = auto_mod.check_from_dictionary(new_word)
                    if check:
                        return True, new_word, similarity
                return False, "", 0
        else:
            combinations = [processed_word]
            for key in auto_mod.var_word_init():
                if key in processed_word:
                    new_combinations = []
                    for variation in auto_mod.var_word_init()[key]:
                        for word in combinations:
                            new_word = processed_word.replace(key, variation)
                            new_word = auto_mod.preprocess_word(new_word)
                            if len(new_word) < 16 and new_word not in new_combinations:
                                new_combinations.append(new_word)
                    combinations = new_combinations
            for new_word in combinations:
                tword, similarity = auto_mod.check_from_levenshtein(processed_word)
                if similarity > 0.70:
                    return True, tword, similarity
            return False, tword, similarity
    
    def check_message(message: str):
        black_word = {}
        black_word_similarity = {}
        message_content = message.split(" ")
        for word in message_content:
            check, true_word, similarity = auto_mod.check_word(word)
            if check:
                black_word[word] = true_word
                black_word_similarity[word] = similarity
        return black_word, black_word_similarity
                

class Data:
    
    def void():
        return
    
class version:
    forward = [1.1, 1.2]
    recommanded = 1.3
    laster = 1.4
    
class Bot:
    
    privates_guilds = [592737567699501147, 969214672215625748, 963051007586213919]

    def console(type, arg):
        startTime = datetime.strftime(datetime.now(), '%H:%M:%S')
        print(f"[{startTime} {type}] {inspect.stack()[1].function}: {arg}")
    
    def Launched(launched_bot):
        launched_bot_class = globals()[launched_bot]
        Bot.Name = launched_bot_class.Name
        Bot.Token = launched_bot_class.__Token__
        Bot.BotGuild = launched_bot_class.BotGuild
        Bot.AnnonceChannel = launched_bot_class.AnnonceChannel
        Bot.ConsoleChannel = launched_bot_class.ConsoleChannel
        Bot.MessageChannel = launched_bot_class.MessageChannel
        Bot.Prefix = launched_bot_class.Prefix

    Name = str()
    Token = str()
    BotGuild = int()
    AnnonceChannel = int()
    ConsoleChannel = int()
    MessageChannel = int()
    Prefix = str()

class BetaBelouga:
    Name= "BetaBelouga"
    __Token__ = "OTY5NTIwOTYyMjIxNTEwNjU2.Ymumwg.YXeEiL-gIwv_A_22t-mS2-jvVNQ"
    BotGuild = 969214672215625748
    AnnonceChannel = 1066680440209027152
    ConsoleChannel = 972036600357879828
    MessageChannel = 1009208789674754098
    Prefix = "BB"

class Belouga:
    Name= "Belouga"
    __Token__ = "OTcxNzUwMzU1NzY1NDM2NDI2.GWTHwA.FmvtUzb9M2DPNX3Pu6A4c4rcEjrnlNvj55uRPI"
    BotGuild = 969214672215625748
    AnnonceChannel = 1066680440209027152
    ConsoleChannel = 972036409085014046
    MessageChannel = 1175569633357598742
    Prefix = "BL"

class GameHub:
    Name = "GameHub"
    __Token__ = "MTEyNDA0NTEwNjU1MTQ1NTc1NA.G7MVDb.S9xyeJatNfRV-TwbhDApZ_ewATFV7CRVQMfpLs"
    BotGuild = 969214672215625748
    AnnonceChannel = 1066680440209027152
    ConsoleChannel = 1016765628180348991
    MessageChannel = 1016765673004867645
    Prefix = "?"
    
