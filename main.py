import wikipedia
from discord.ext import commands
from random import randint, choice
import string
from os import environ
import sqlite3

client = commands.Bot(command_prefix="!")
conn = sqlite3.connect('saves.db')
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS saves (key varchar(14), msg text);")


def get_keys(filename):
    cursor.execute("SELECT key FROM saves;")
    return [i[0] for i in cursor.fetchall()]


def generate_raw_key(stringLength=12):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(stringLength))


def generate_key(filename):
    bla = generate_raw_key()
    keys = get_keys(filename)
    while bla in keys:
        bla = generate_raw_key()
    return bla


@client.event
async def on_ready():
    print("Online!")


@client.command(brief="Gives you ping latency in miliseconds")
async def ping(ctx):
    await ctx.send("Ping is {}ms".format(round(client.latency * 1000)))


@client.command(brief="Saves snippet of text in file, gives you the key. Get keys with !keys, loads message with !load. (!save [text])")
async def save(ctx, *, msg):
    key = generate_key("saves.db")
    cursor.execute(
        "INSERT INTO saves (key, msg) VALUES (?, ?); ", (key, msg))
    conn.commit()
    await ctx.send("Your unique key is: " + key)


@client.command(brief="Loads text stored by save. (!load [key])")
async def load(ctx, key):
    try:
        cursor.execute("SELECT msg FROM saves WHERE key=?", (key,))
        await ctx.send("`{}`".format(cursor.fetchone()[0]))
    except Exception as e:
        pass


@client.command(brief="Gives you summary of given query. (!wiki [query])")
async def wiki(ctx, *, text):
    try:
        await ctx.send("`{}`".format(wikipedia.summary(text, auto_suggest=False)))
    except Exception as e:
        await ctx.send("```{}```".format(e))


@client.command(brief="Prints all the keys. (!keys)")
async def keys(ctx):
    keys = get_keys("saves.db")
    msg = "\n".join(keys)
    await ctx.send("List of keys:\n" + msg)


@client.command(brief="Rolls a dice and gives you the result between 1 and 6. (!roll)")
async def roll(ctx):
    await ctx.send("Rolling a dice: {}".format(randint(1, 6)))


@client.command(brief="Chooses between texts, texts are separated by ;. example: !choose bla; bla1;bla2. (!choose [text];...)")
async def choose(ctx, *, sol):
    print(sol)
    soll = choice(sol.split(";"))
    await ctx.send("My choice is: {}".format(soll))


@client.command(brief="Clears all text in channel")
async def clear(ctx):
    await ctx.channel.purge()

client.run(environ.get("DISCORD_SECRET_KEY"))
