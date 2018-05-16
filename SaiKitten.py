import discord
from discord import Server
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import requests
import sys
import json
import datetime
from pathlib import Path
from anime import anime
from osu import osu
import re

#read key from file
key = json.load(open('key.txt'))

osuapi = "https://osu.ppy.sh/api/get_beatmaps?k=" + str(key['osu'])

modes = ['osu','taiko','fruits','mania']

#declare command prefix
bot = commands.Bot(command_prefix='$$')

#remove default help command
bot.remove_command('help')

#when bot initialised, change game and print bot details to screen
@bot.event
async def on_ready():
    await bot.change_presence(game = discord.Game(name='with Mom'))
    global me
    me = await bot.get_user_info('155421790963892224')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')

#
# --COMMANDS--
#If message starts with command prefix, read command word and reply
#

@bot.command(pass_context = True)
async def clear(ctx):
    if ctx.message.author == me: await bot.purge_from(Server.get_channel(ctx.message.server,'431806042377289739'))
    else: await bot.say("You are not permitted to do that")

@bot.command(pass_context = True)
async def help(ctx):
    await bot.say("```Commands:\n\t$$a <anime name> - Get information on anime\n\t$$boost - boost\n\t$$BOOST - BOOST\n\t$$help - How did you get here?\n\t$$trap - <:jack:403983194996736031>```")

@bot.command(pass_context = True)
async def boost(ctx):
    await bot.say("https://b.catgirlsare.sexy/QwAa.jpg")

@bot.command(pass_context = True)
async def BOOST(ctx):
    await bot.say("https://i.imgur.com/Yvf3htW.gif")

@bot.command(pass_context = True)
async def trap(cxt):
    await bot.say("<:jack:403983194996736031>")

#Split message by new line, pop first element in list, split again by spaces.
#Delete command from message and join elements with a space between each.
#Call anime function and send info to discord.
@bot.command(pass_context = True)
async def a(ctx):
    split_message = ctx.message.content.split('\n').pop(0).split(' ')
    del split_message[0]
    split_message = ' '.join(split_message)
    #if fail DM error to me
    try:
        embed = anime(split_message)
        await bot.say(embed=embed)
    except Exception as err:
        await bot.send_message(me,"Uuwahh! Senpai! Something broke!\n ``` " + str(err) + " ```")

#
# --COMMANDS END--
#

@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        if 'osu.ppy.sh/beatmapsets' in message.content:
            osumsg = [e for e in re.split('[/#]',message.content.split('beatmapsets/').pop(1)) if e not in modes]
            try:
                embed = osu(osumsg,key['osu'])
                await bot.send_message(message.channel,embed=embed)
            except Exception as err:
                await bot.send_message(me,"Uuwahh! Senpai! Something broke!\n ``` " + str(err) + " ```")
    await bot.process_commands(message)

bot.run(str(key["discord"]))
