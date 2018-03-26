import discord
import requests
anilist = 'https://graphql.anilist.co'
def anime(split_message):
    #file = Path("anime" + split_message + ".txt")
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
    return embed
