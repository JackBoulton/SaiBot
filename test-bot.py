import discord
from discord import Server
from discord import Client
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio

bot = commands.Bot(command_prefix='$')
key = open('testkey.txt').readline().rstrip('\n')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')
    #
    #tests begin here
    #
    global chan
    chan = bot.get_channel('431806042377289739')


@bot.command(pass_context = True)
async def test(ctx):
    await bot.send_message(chan, '$$a flcl')
    await bot.send_message(chan, 'https://osu.ppy.sh/beatmapsets/717528#osu/1515830')
    await bot.send_message(chan, 'https://osu.ppy.sh/beatmapsets/591442')
    await bot.send_message(chan, '$$v remo con || wan opo')
    await bot.send_message(chan, '$$v a || yunosuke')
    await bot.send_message(chan, '$$v s || lazy')
    await bot.send_message(chan, '$$v a || hgsbgshjgj')
    await bot.send_message(chan, '$$v s || jkgbksdjgbs')
    await bot.send_message(chan, '$$v dfkjbfd || nfsjbgfg')
    await bot.send_message(chan, '$$v cat life || jhbsdgsd')
    await bot.send_message(chan, '$$v undead enemy')
    await bot.send_message(chan, '$$v a ||')



bot.run(key)
