import wikipedia
from discord.ext import commands
import discord
from urllib.parse import unquote
from random import randint, choice
import string
import requests
from os import environ
import csv

DICE_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/2/2c/Alea_1.png",
    "https://upload.wikimedia.org/wikipedia/commons/b/b8/Alea_2.png",
    "https://upload.wikimedia.org/wikipedia/commons/2/2f/Alea_3.png",
    "https://upload.wikimedia.org/wikipedia/commons/8/8d/Alea_4.png",
    "https://upload.wikimedia.org/wikipedia/commons/5/55/Alea_5.png",
    "https://upload.wikimedia.org/wikipedia/commons/f/f4/Alea_6.png"
]

client = commands.Bot(command_prefix="c!")
LANG = "en"

with open('descriptions.csv', 'r') as file:
    DESCRIPTIONS = dict(csv.reader(file, delimiter="\t"))


def get_wiki(query, lang):
    if lang != "en":
        url = f"https://{lang}.wikipedia.org/wiki/{query}"
        query = requests.get(url)
        query = unquote(query.url.split("/")[-1])

    wiki_page = wikipedia.page(query, auto_suggest=False)

    embed = discord.Embed(
        title=wiki_page.title,
        url=wiki_page.url,
        description=wiki_page.summary
    )
    embed.add_field(name="Language", value=lang)
    embed.set_footer(text="c!lang to change language")
    return embed


@client.event
async def on_ready():
    print("Online!")


@client.command(brief=DESCRIPTIONS["ping"])
async def ping(ctx):
    await ctx.send("Ping is {}ms".format(round(client.latency * 1000)))


@client.command(brief=DESCRIPTIONS["lang"])
async def lang(ctx, language):
    global LANG
    LANG = language
    print(LANG)
    wikipedia.set_lang(language)


@client.command(brief=DESCRIPTIONS["wiki"])
async def wiki(ctx, *, text):
    try:
        embed = get_wiki(text, lLANGang_code)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("```{}```".format(e))


@client.command(brief=DESCRIPTIONS["roll"])
async def roll(ctx):
    await ctx.send(DICE_IMAGES[randint(0, 5)])


@client.command(brief=DESCRIPTIONS["choose"])
async def choose(ctx, *, sol):
    print(sol)
    soll = choice(sol.split(";"))
    await ctx.send("My choice is: {}".format(soll))


@client.command(brief=DESCRIPTIONS["clear"])
async def clear(ctx):
    await ctx.channel.purge()


@client.command(brief=DESCRIPTIONS["ban"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User):
    await ctx.guild.ban(user)


client.run(environ.get("DISCORD_SECRET_KEY"))
