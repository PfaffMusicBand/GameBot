"""
Modul automod
--------------
Système d'automod du bot.
Pour plus d'info:
>>> automod.AutoMod
"""
from Levenshtein import distance
from collections import defaultdict

class AutoMod:
    """
    AutoMod
    --------
    Système d'automodération adaptatif
    
    Utilisation
    -------------
    Prend en entrée une liste de mots et donne en sortie une liste de mots considérés comme grossiers ainsi que la similarité entre le mot du message et le mot avec lequel il est comparé.
    
    Exemple
    --------
    >>> AutoMod.check_message(message) -> black_word["mot_du_message"] = "mot_trouvé", black_word_similarity["mot_du_message"] = float(similarité des mots de 0 à 1)
    >>> AutoMod.check_message("sale puttteux") -> black_word["puttteux"] = "pute", black_word_similarity["puttteux"] = 0.43
    """
    black_liste = []

    @staticmethod
    def check_word_init():
        with open("Packs/blackword.txt", "r", encoding="utf-8") as data:
            return [ligne.strip() for ligne in data]

    @staticmethod
    def var_word_init():
        variation = defaultdict(list)
        with open("Packs/blackwordvariation.txt", "r", encoding="utf-8") as data:
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