import wikipedia
from discord.ext import commands
import discord
from urllib.parse import unquote
from random import randint, choice
import string
import requests
from os import environ
import sqlite3
import csv

CREATE_TABLE_Q = "CREATE TABLE IF NOT EXISTS saves (key varchar(14), msg text);"
SELECT_KEY_Q = "SELECT key FROM saves;"
INSERT_INTO_Q = "INSERT INTO saves (key, msg) VALUES (?, ?);"
SELECT_MSG_BY_KEY_Q = "SELECT msg FROM saves WHERE key=?"

DICE_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/2/2c/Alea_1.png",
    "https://upload.wikimedia.org/wikipedia/commons/b/b8/Alea_2.png",
    "https://upload.wikimedia.org/wikipedia/commons/2/2f/Alea_3.png",
    "https://upload.wikimedia.org/wikipedia/commons/8/8d/Alea_4.png",
    "https://upload.wikimedia.org/wikipedia/commons/5/55/Alea_5.png",
    "https://upload.wikimedia.org/wikipedia/commons/f/f4/Alea_6.png"
]

client = commands.Bot(command_prefix="c!")
cursor = conn.cursor()
cursor.execute(CREATE_TABLE_Q)
lang_code = "en"

with open('descriptions.csv', 'r') as file:
    descriptions = dict(csv.reader(file, delimiter="\t"))


@client.event
async def on_ready():
    print("Online!")


@client.command(brief=descriptions["ping"])
async def ping(ctx):
    await ctx.send("Ping is {}ms".format(round(client.latency * 1000)))


@client.command(brief=descriptions["lang"])
async def lang(ctx, language):
    global lang_code
    lang_code = language
    print(lang_code)
    wikipedia.set_lang(language)


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


@client.command(brief=descriptions["wiki"])
async def wiki(ctx, *, text):
    try:
        embed = get_wiki(text, lang_code)
        for i in dir(client) + dir(ctx):
            if "server" in i or "say" in i:
                print(i)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("```{}```".format(e))


@client.command(brief=descriptions["keys"])
async def keys(ctx):
    keys = get_keys("saves.db")
    msg = "\n".join(keys)
    await ctx.send("List of keys:\n" + msg)


@client.command(brief=descriptions["roll"])
async def roll(ctx):
    await ctx.send(DICE_IMAGES[randint(1, 6)])


@client.command(brief=descriptions["choose"])
async def choose(ctx, *, sol):
    print(sol)
    soll = choice(sol.split(";"))
    await ctx.send("My choice is: {}".format(soll))


@client.command(brief=descriptions["clear"])
async def clear(ctx):
    await ctx.channel.purge()

client.run(environ.get("DISCORD_SECRET_KEY"))
