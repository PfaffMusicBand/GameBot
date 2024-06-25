import discord
import os
import re
import Botloader
from discord.ext import commands
from gtts import gTTS
from datetime import datetime

class SendMessageAction:
    def __init__(self, content):
        self.content = content
    async def execute(self, ctx):
        await ctx.send(self.content)

class GenerateMP3Action:
    def __init__(self, text, lang='fr'):
        self.text = text
        self.lang = lang
    async def execute(self, ctx):
        startTime = datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
        tts = gTTS(text=self.text, lang=self.lang)
        output_filename = f'{ctx.guild.id}_{startTime}_output.mp3'
        if os.path.exists(output_filename):
            i = 2
            while os.path.exists(f'{ctx.guild.id}_{startTime}_{i}_output.mp3'):
                i += 1
            output_filename = f'{ctx.guild.id}_{startTime}_{i}_output.mp3'  
        tts.save(output_filename)
        await ctx.send(file=discord.File(output_filename))
        os.remove(output_filename)

def parse_actions(actions: str):
    action_list = []
    actions = actions.strip()
    
    if '&' in actions:
        action_strs = actions.split('&')
    else:
        action_strs = [actions]

    def check_secondary(content: str):
        calc_pattern = r'Calc\((.*?)\)'
        matches = re.findall(calc_pattern, content)
        for calc_expression in matches:
            try:
                result = eval(calc_expression)
                content = content.replace(f'Calc({calc_expression})', str(result))
            except Exception as e:
                Botloader.Bot.console("WARN", f"Erreur lors de l'évaluation de {calc_expression}: {e}")
        return content
    for action_str in action_strs:
        send_message_match = re.match(r'SendMessage\{(.*?)\}', action_str)
        generate_mp3_match = re.match(r'GenerateMP3\{(.*?)\}', action_str)
        print(action_str)
        if send_message_match:
            content = send_message_match.group(1)
            result = check_secondary(content)
            if result:
                action_list.append(SendMessageAction(result))
            else:
                action_list.append(SendMessageAction(content))
        
        elif generate_mp3_match:
            params = generate_mp3_match.group(1)
            txt, lg = params.split(";")
            result = check_secondary(txt)
            if result:
                action_list.append(GenerateMP3Action(result, lg))
            else:
                action_list.append(GenerateMP3Action(txt, lg))
    
    return action_list
