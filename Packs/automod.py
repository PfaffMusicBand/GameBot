import requests
from Packs.Botloader import Bot

class AutoMod:
    """
    API Automod
    -----------
    API pour l'auto-modération

    ENDPOINTS
    --------
    >>> `/check_message` -> "black_word":{"message_word":"true_word"}, "black_word_similarity":{"message_word":"similarity"}, "version":"version"
    >>> `/version` -> "version":"version"

    FONCTIONS
    ---------

    >>> `check_message(message)` -> bw={"message_word":"true_word"}, bws={"message_word":"similarity"}
    >>> `version()` -> v="version format x.x.x"

    Exemple
    -------
    >>> bw, bws = check_message(message)
    >>> for key in blw:
    >>>     print(f"Mot {key} détecté: {round(blws[key], 2) * 100}% de ressemblance avec {blw[key]}.")
    """
    API_KEY = 'your_api_key'

    def check_message(message: str):
        api_url = 'http://automod.smaugue.lol:5000/check_message'
        data = {'message': message}
        headers = {'x-api-key': AutoMod.API_KEY}

        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            bw = response_data.get('black_word')
            bws = response_data.get('black_word_similarity')
        else:
            Bot.console("ERROR", f"Erreur {response.status_code}: {response.text}")
            bw = {}
            bws = {}
        return bw, bws

    def automod_version():
        api_url = 'http://automod.smaugue.lol:5000/version'
        headers = {'x-api-key': AutoMod.API_KEY}
        response = requests.post(api_url, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            v = response_data.get('version')
        else:
            Bot.console("ERROR", f"Erreur {response.status_code}: {response.text}")
            v = 'uncknow'
        return v
