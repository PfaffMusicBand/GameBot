import requests
from Packs.Botloader import Bot

class AutoMod:
    API_KEY = 'smaugue_jp56tkJ6LTk8SF94OPs1zRbSHG8pvvtO'

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
