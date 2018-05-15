import discord
import requests
from pathlib import Path
import json
import datetime

modes = ['osu','taiko','fruits','mania']

def osu(osumsg):
    file = Path("osu\\beatmapset_" + osumsg[0] + ".txt")
    if file.is_file() is False:
        r = requests.post(osuapi + "&s=" + osumsg[0])
        with open(file,'w+') as newfile:
            json.dump(r.json(),newfile,indent=4)
            newfile.close()

    osudata = json.load(open(file))
    embed = discord.Embed(title=osudata[0]['title'])
    embed.set_thumbnail(url="https://b.ppy.sh/thumb/" + osudata[0]['beatmapset_id'] + ".jpg")
    embed.add_field(name="Duration",value = str(datetime.timedelta(seconds=int(osudata[0]['total_length']))),inline=False)
    for x in osudata:
        try:
            if x['beatmap_id'] == osumsg[1] and osumsg[1] != '':
                embed.add_field(name="Circle Size",value = x['diff_size'],inline=True)
                embed.add_field(name="OD", value = x['diff_overall'],inline=True)
                embed.add_field(name="AR",value = x['diff_approach'], inline=True)
                embed.add_field(name="SR", value = round(float(x['difficultyrating']),2),inline=True)
            else:
                raise Exception
        except:
            embed.add_field(name="Mode - Star - Diff", value = modes[int(x['mode'])] + " - " + str(round(float(x['difficultyrating']),2)) + " - " + x['version'],inline = False)
    embed.add_field(name="Audio Clip", value ="https://b.ppy.sh/preview/" + osudata[0]['beatmapset_id'] + ".mp3",inline=False)
    embed.add_field(name="Download" , value = "https://osu.ppy.sh/beatmapsets/" + osudata[0]['beatmapset_id'] + "/download",inline=True)
    return embed
