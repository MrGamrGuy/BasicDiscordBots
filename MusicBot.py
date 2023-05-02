import discord
from discord.ext import commands
import youtube_dl

client = commands.Bot(command_prefix='!')

queue = []

@client.command()
async def q(ctx, url):
    channel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not voice:
        voice = await channel.connect()

    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        url = info['formats'][0]['url']
        title = info['title']

    queue.append((url, title))

    if not voice.is_playing():
        play_next(ctx, voice)

def play_next(ctx, voice):
    if len(queue) > 0:
        url, title = queue.pop(0)

        print(f"Now playing: {title}")

        voice.play(discord.FFmpegPCMAudio(url), after=lambda _: play_next(ctx, voice))
        voice.is_playing()
    else:
        print("Queue empty")

@client.command()
async def queue(ctx):
    queue_message = "Queue:\n"
    for i, (url, title) in enumerate(queue):
        queue_message += f"{i+1}. {title}\n"

    await ctx.send(queue_message)

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not voice:
        voice = await channel.connect()

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.pause()

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        voice.resume()

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()

@client.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not voice:
        voice = await channel.connect()

    with youtube_dl.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        url = info['formats'][0]['url']

    voice.play(discord.FFmpegPCMAudio(url))
    
    client.run('TOKEN')
