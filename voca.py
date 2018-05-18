import json
import requests
import re
import discord
import datetime

vocaapi = "https://vocadb.net/api/"

def voca(vocamsg):
    try:
        if vocamsg[0] != "a":
            if vocamsg[0] == "s":
                r = requests.get(vocaapi + "songs?query=" + vocamsg[1] + "&maxResults=1&sort=RatingScore&nameMatchMode=Auto&fields=Artists,ThumbUrl,PVs,Tags&lang=English").json()['items'][0]
            else:
                rs = requests.get(vocaapi + "songs?query=" + vocamsg[0] + "&sort=RatingScore&nameMatchMode=Auto&fields=Artists,ThumbUrl,PVs,Tags&lang=English").json()['items']
                if not rs:
                    return Exception("NoValue")
                ra = requests.get(vocaapi + "artists?query=" + vocamsg[1] + "&nameMatchMode=Auto&lang=English&sort=FollowerCount").json()['items']

                output = []
                for s in rs:
                    for sa in s['artists']:
                        for a in ra:
                            try:
                                if a['id'] == sa['artist']['id']:
                                    row = [s['id'],a['id'],s['ratingScore']]
                                    output.append(row)
                                    break
                            except KeyError: continue
                try:
                    r = [r for r in rs if output[0][0] == r['id']][0]
                except: r = rs[0]

            tags = []
            pvs = []
            for t in range(5):
                try:
                    tags.append(sorted(r['tags'],key=lambda tag: tag['count'],reverse=True)[t]['tag']['name'])
                except IndexError: break
            for p in r['pvs']:
                if p['pvType'] == "Original":
                    pvs.append(p['url'])
            tags.sort(reverse=True)
            embed = discord.Embed(title=r['name'] + ' - ' + r['artistString'],url="https://vocadb.net/S/"+str(r['id']))
            embed.set_thumbnail(url=r['thumbUrl'])
            embed.add_field(name="Type",value = r['songType'])
            embed.add_field(name="Duration",value=str(datetime.timedelta(seconds=int(r['lengthSeconds']))))
            embed.add_field(name="Tags",value=", ".join(tags))
            embed.add_field(name="PV",value="\n".join(pvs))
        elif vocamsg[0] == "a":
            r = requests.get(vocaapi + "artists?query=" + vocamsg[1] + "&fields=Tags,MainPicture&maxResults=1&nameMatchMode=Auto&lang=English&sort=FollowerCount").json()['items'][0]
            tags = []
            for t in range(5):
                try:
                    tags.append(sorted(r['tags'],key=lambda tag: tag['count'],reverse=True)[t]['tag']['name'])
                except IndexError: break
            embed = discord.Embed(title=r['name'] + ", " + r['defaultName'],url="https://vocadb.net/Ar/"+str(r['id']))
            embed.set_thumbnail(url=r['mainPicture']['urlTinyThumb'])
            embed.add_field(name="Type",value = r['artistType'])
            embed.add_field(name="Tags",value=", ".join(tags))
        return embed
    except IndexError: return Exception("NoValue")
