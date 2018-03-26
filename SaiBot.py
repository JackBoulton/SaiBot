import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import requests
import sys
from pathlib import Path

anilist = 'https://graphql.anilist.co'
key = 'NDIyNzI1NTU0OTU3OTc1NTUy.DZHYpw.RJMw32fyUufJe7pTlQV_JTkHg0k'

bot = commands.Bot(command_prefix='$$')

@bot.event
async def on_ready():
    await bot.change_presence(game = discord.Game(name='with catnip'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')

@bot.command(pass_context = True)
async def BOOST(ctx):
    await bot.say("https://i.imgur.com/Yvf3htW.gif")

@bot.command(pass_context = True)
async def trap(cxt):
    await bot.say("<:jack:403983194996736031>")

@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        if 'osu.ppy.sh' in message.content:
                await bot.send_message(message.channel, 'Work in progress')
    await bot.process_commands(message)

@bot.command(pass_context = True)
async def boost(ctx):
    await bot.say("https://b.catgirlsare.sexy/QwAa.jpg")

@bot.command(pass_context = True)
async def a(ctx):
    split_message = ctx.message.content.split('\n').pop(0).split(' ')
    #split_message = ctx.message.content.split(' ')
    del split_message[0]
    split_message = ' '.join(split_message)
    file = Path("anime" + split_message + ".txt")
    query = '''
    query($title: String){
        Media (search: $title, type : ANIME, sort : SEARCH_MATCH){
            id
            title{
                romaji
                english
                native
            }
            description
            averageScore
            coverImage{
                medium
            }
        }
    }
    '''

    variables = {
        'title' : split_message
    }

    r = requests.post(anilist, json={'query':query, 'variables': variables})
    headers = r.headers
    response = r.json()

    print(headers)

    english = response['data']['Media']['title']['english']
    native = response['data']['Media']['title']['native']

    if not response['data']['Media']['title']['english'] : english = '-'

    if not response['data']['Media']['title']['native'] : native = '-'

    desc = response['data']['Media']['description'].replace('<br>','')

    embed=discord.Embed(title=response['data']['Media']['title']['romaji'], description=desc, color=0x02A9FF)
    embed.set_thumbnail(url=response['data']['Media']['coverImage']['medium'])
    embed.add_field(name="Romaji", value=response['data']['Media']['title']['romaji'], inline=True)
    embed.add_field(name="English", value=english, inline=True)
    embed.add_field(name="Native", value=native, inline=True)
    embed.add_field(name="Score", value=response['data']['Media']['averageScore'],inline=True)
    embed.add_field(name="Link", value = "http://anilist.co/anime/" + str(response['data']['Media']['id']),inline=True)
    await bot.say(embed=embed)

bot.run(key)
