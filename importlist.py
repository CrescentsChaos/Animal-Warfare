import os
import discord
from discord.ext import commands
from discord import File
from discord import app_commands
import aiosqlite
import random
import datetime
import requests
import time
import os
import random
import asyncio
import math
import datetime
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

load_dotenv()
token=os.getenv("TOKEN")
intents = discord.Intents.default()
# Only turn on what you actually need:
intents.message_content = False   # True only if you read normal messages
intents.members = False           # True only if you access member lists
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
    
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Game("with life"))
    print(f"We have logged in as {bot.user}")
    try:
        synced=await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
    except:
        print(Exception)
        