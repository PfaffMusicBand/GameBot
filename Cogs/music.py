import discord
import yt_dlp as youtube_dl
import spotipy
import asyncio
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext.commands import Context

SPOTIPY_CLIENT_ID = '0b765387d7be48d0bd4729cca6e4c07c'
SPOTIPY_CLIENT_SECRET = 'fa3ebceeaa3c4a4693eef2c6a0c0f47b'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    #'proxy': 'https://176.148.176.111'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @commands.hybrid_command(name='join', help='Fait rejoindre le bot à un canal vocal')
    async def join(self, ctx):
        await self.ljoin(ctx)

    async def ljoin(self, ctx:Context, *, ir="y"):
        if not ctx.author.voice:
            await ctx.send("Vous n'êtes pas connecté à un canal vocal.")
            return False
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            if ctx.voice_client.channel == channel:
                return True
            if ctx.voice_client.is_playing() or len(self.queue) > 0:
                await ctx.send("Le bot est déjà en cours d'utilisation.")
                return False
            else:
                await ctx.voice_client.disconnect()
        await channel.connect(self_deaf=True)
        if ir == "n":
            await ctx.channel.send(f'Connecté à {channel.name}.')
        else:
            await ctx.send(f'Connecté à {channel.name}.')
        return True

    @commands.hybrid_command(name='leave', help='Fait quitter le bot du canal vocal')
    async def leave(self, ctx):
        if not ctx.voice_client:
            await ctx.send("Le bot n'est pas connecté à un canal vocal.")
            return
        await ctx.voice_client.disconnect()

    @commands.hybrid_command(name='pause', help='Met en pause la musique en cours')
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Musique en pause.")

    @commands.hybrid_command(name='resume', help='Reprend la musique en cours')
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Reprise de la musique.")

    @commands.hybrid_command(name='skip', help='Arrête la musique en cours')
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Voix arrêtée.")

    @commands.hybrid_command(name='queue', help='Affiche la file d\'attente')
    async def show_queue(self, ctx):
        if len(self.queue) == 0:
            await ctx.send("La file d'attente est vide.")
        else:
            queue_titles = [player['title'] for player in self.queue]
            await ctx.send('\n'.join(queue_titles))

    @commands.hybrid_command(name='fplay', help='fplay')
    async def fplay(self, ctx: commands.Context):
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)
    @commands.hybrid_command(name='play', help='Joue une musique à partir d\'une URL YouTube ou Spotify')
    async def play(self, ctx: commands.Context, url):
        if await self.ljoin(ctx, ir="n") is False:
            return

        async with ctx.typing():
            if "https://" not in url:
                url = await self.search_youtube(url)
                if not url:
                    await ctx.send("Aucune vidéo trouvée pour cette recherche.")
                    return

            if "spotify.com" in url:
                tracks = await self.get_spotify_tracks(url)
                if not tracks:
                    await ctx.send("Aucune piste trouvée pour cette playlist Spotify.")
                    return
                for track_url in tracks:
                    self.queue.append({'url': track_url, 'title': track_url})
                    await ctx.send(f"{track_url} ajouté à la liste.")
            elif "youtube.com/playlist" in url or "list=" in url:
                playlist_urls = await self.get_youtube_playlist_urls(url)
                for video_url in playlist_urls:
                    self.queue.append({'url': video_url, 'title': video_url})
                    await ctx.send(f"{video_url} ajouté à la liste.")
            else:
                self.queue.append({'url': url, 'title': url})
                print("python ca pue la merde, discord ca pue la merde, youtube ca pue la merde")
                await ctx.send(f"{url} ajouté à la liste.")

        if not ctx.voice_client.is_playing():
            print("la queue de merde de fsp de python qui pue")
            print(self.queue)
            await self.play_next(ctx)

    async def play_next(self, ctx):
        #if len(self.queue) > 0:
        url = self.queue.pop(0)['url']
        await ctx.send("Chargement de la musique...")
        player = await self.YTDLSource.from_url(url, loop=self.bot.loop, stream=False)
        if player is None:
            await ctx.send("Erreur lors du téléchargement de la vidéo. Passage à la suivante...")
            await self.play_next(ctx)
            return
        if ctx.voice_client is None:
            return
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop).result())
        await ctx.send(f"Lecture de : {player.title}")
        #else:
        #    await ctx.send("La file d'attente est vide.")

    async def get_spotify_tracks(self, url):
        tracks = []
        if "track" in url:
            track_id = url.split("/")[-1].split("?")[0]
            track = sp.track(track_id)
            track_name = f"{track['name']} {track['artists'][0]['name']}"
            youtube_url = await self.search_youtube(track_name)
            if youtube_url:
                tracks.append(youtube_url)
        elif "playlist" in url:
            playlist_id = url.split("/")[-1].split("?")[0]
            results = sp.playlist(playlist_id)
            for item in results['tracks']['items']:
                track = item['track']
                track_name = f"{track['name']} {track['artists'][0]['name']}"
                youtube_url = await self.search_youtube(track_name)
                if youtube_url:
                    tracks.append(youtube_url)
        return tracks

    async def get_youtube_playlist_urls(self, url):
        ydl_opts = {
            'extract_flat': True,
            'playlistend': 100,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if 'entries' in info_dict:
                video_urls = [f"https://www.youtube.com/watch?v={entry['id']}" for entry in info_dict['entries']]
                return video_urls
            else:
                return []

    async def search_youtube(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'default_search': 'ytsearch',
            'quiet': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if 'entries' in info and info['entries']:
                    return f"https://www.youtube.com/watch?v={info['entries'][0]['id']}"
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
                if 'url' in data:
                    filename = data['url'] if stream else ytdl.prepare_filename(data)
                    return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
            except Exception as e:
                print(f"Une erreur s'est produite lors de l'extraction YouTube: {e}")
                return None