import discord
import yt_dlp as youtube_dl
import spotipy
import asyncio
import os
import Botloader
from discord.ext.commands import Context
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = '0b765387d7be48d0bd4729cca6e4c07c'
SPOTIPY_CLIENT_SECRET = 'fa3ebceeaa3c4a4693eef2c6a0c0f47b'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

files = []

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class Music(commands.Cog):
    '''
    Ya ennormément de bug à corrigé dans le style des vérification de l'état du voice_client avant de faire quelque chose
    '''
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    async def play_next(self, ctx):
        if len(self.queue) > 0:
            player = self.queue.pop(0)
            ctx.voice_client.play(player, after=lambda e:  asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop).result())
            await ctx.channel.send(f'Lecture de : {player.title}')
            files.append(player.filename)
        else:
            ctx.voice_client.stop()
            await ctx.channel.send('La file d\'attente est vide.')
            for file in files:
                try:
                    os.remove(file)
                    del(files[0])
                    Botloader.Bot.console("INFO", f"File delete: {file}")
                except Exception as e: Botloader.Bot.console("WARN", f"Error: {e}")


    @commands.hybrid_command(name='join', help='Fait rejoindre le bot à un canal vocal')
    async def join(self, ctx):
        await Music.ljoin(self, ctx)

    async def ljoin(self, ctx: Context,*,ir = "y"):
        if not ctx.message.author.voice:
            await ctx.send(f"Vous n'êtes pas connectez à un channel vocal.")
            return False
        channel = ctx.message.author.voice.channel
        if ctx.voice_client:
            if ctx.voice_client.is_playing() or len(self.queue) > 0:
                await ctx.send("Le bot est déjà en cour d'utilisation.")
                return False
            else: await ctx.voice_client.disconnect()
        await channel.connect(self_deaf=True)
        if ir == "y":
            await ctx.send(f'Connecté à {channel.name}.')
        else: await ctx.channel.send(f'Connecté à {channel.name}.')
        return True

    @commands.hybrid_command(name='leave', help='Fait quitter le bot du canal vocal')
    async def leave(self, ctx):
        if not ctx.voice_client:
            await ctx.send('Le bot n\'est pas connecté à un canal vocal.')
            return
        await ctx.voice_client.disconnect()

    @commands.hybrid_command(name='play', help='Joue une musique à partir d\'une URL YouTube')
    async def play(self, ctx: Context, url):
        if await Music.ljoin(self,ctx,ir="n") is False:
            return
        async with ctx.typing():
            if "https://" not in url:
                url = await self.search_youtube(url)
                if not url:
                    await ctx.channel.send('Aucune vidéo trouvée pour cette recherche.')
                    return
            player = await self.YTDLSource.from_url(url, loop=self.bot.loop, stream=False)
            if player is None:
                await ctx.channel.send('Erreur lors du téléchargement de la vidéo.')
                return
            self.queue.append(player)
            await ctx.send(f"{player.title} ajouté à la liste.")
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    @commands.hybrid_command(name='pause', help='Met en pause la musique en cours')
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('Musique en pause.')

    @commands.hybrid_command(name='resume', help='Reprend la musique en cours')
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('Reprise de la musique.')

    @commands.hybrid_command(name='stop', help='Arrête la musique en cours')
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('Musique arrêtée.')

    @commands.hybrid_command(name='queue', help='Affiche la file d\'attente')
    async def show_queue(self, ctx):
        if len(self.queue) == 0:
            await ctx.send('La file d\'attente est vide.')
        else:
            queue_titles = [player.title for player in self.queue]
            await ctx.send('\n'.join(queue_titles))

    async def search_youtube(self, query):
        try:
            info = await self.bot.loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{query}", download=False))
            if 'entries' in info and len(info['entries']) > 0:
                return info['entries'][0]['webpage_url']
            else:
                return None
        except Exception as e:
            print(f"Une erreur s'est produite lors de la recherche YouTube: {e}")
            return None

    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get('title')
            self.url = data.get('url')
            self.filename = ytdl.prepare_filename(data)
            self.duration = data.get('duration')


        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            loop = loop or asyncio.get_event_loop()
            try:
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

                if 'entries' in data:
                    data = data['entries'][0]

                filename = data['url'] if stream else ytdl.prepare_filename(data)
                return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
            except Exception as e:
                print(f"Erreur lors de l'extraction de l'info YouTube: {e}")
                return None
