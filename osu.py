import discord
import requests
from pathlib import Path
import json
import datetime

modes = ['osu','taiko','fruits','mania']

def osu(osumsg,key):
    osuapi = "https://osu.ppy.sh/api/get_beatmaps?k=" + str(key)
    file = Path("osu\\beatmapset_" + osumsg[0] + ".txt")
    if file.is_file() is False:
        r = requests.post(osuapi + "&s=" + osumsg[0])
        with file.open('w+') as newfile:
            json.dump(r.json(),newfile,indent=4)
            newfile.close()

    osudata = json.load(file.open())
    embed = discord.Embed(title=osudata[0]['title'])
    embed.set_thumbnail(url="https://b.ppy.sh/thumb/" + osudata[0]['beatmapset_id'] + ".jpg")
    embed.add_field(name="Duration",value = str(datetime.timedelta(seconds=int(osudata[0]['total_length']))),inline=False)
    for x in osudata:
        try:
            if osumsg[1] == '':
                raise Exception
            elif x['beatmap_id'] == osumsg[1]:
                embed.add_field(name="Circle Size",value = x['diff_size'],inline=True)
                embed.add_field(name="OD", value = x['diff_overall'],inline=True)
                embed.add_field(name="AR",value = x['diff_approach'], inline=True)
                embed.add_field(name="SR", value = round(float(x['difficultyrating']),2),inline=True)
        except:
            embed.add_field(name="Mode - Star - Diff", value = modes[int(x['mode'])] + " - " + str(round(float(x['difficultyrating']),2)) + " - " + x['version'],inline = False)
    embed.add_field(name="Audio Clip", value ="https://b.ppy.sh/preview/" + osudata[0]['beatmapset_id'] + ".mp3",inline=False)
    embed.add_field(name="Download" , value = "https://osu.ppy.sh/beatmapsets/" + osudata[0]['beatmapset_id'] + "/download",inline=True)
    return embed
