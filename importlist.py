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
import sys
import random
import asyncio
import math
import datetime
import json
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

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

WEATHER_FILE = "weather.json"

# 🎲 weighted random choice
def weighted_choice(probabilities: dict) -> str:
    roll = random.random()
    cumulative = 0
    for weather, chance in probabilities.items():
        cumulative += chance
        if roll <= cumulative:
            return weather
    return list(probabilities.keys())[-1]  # fallback

# 🔄 cycle weather for all biomes
async def cycle_weather(interval_hours: int = 3):
    while True:
        try:
            # load current weather file
            with open(WEATHER_FILE, "r") as f:
                data = json.load(f)

            # roll new weather for each biome
            for biome, info in data.items():
                probs = info["probabilities"]
                new_weather = weighted_choice(probs)
                data[biome]["current"] = new_weather

            # save updated weather
            with open(WEATHER_FILE, "w") as f:
                json.dump(data, f, indent=2)

            print("🌍 Weather updated!")
            for biome, info in data.items():
                print(f" - {biome}: {info['current']}")

        except Exception as e:
            print("❌ Weather cycle error:", e)

        # wait until next cycle
        await asyncio.sleep(interval_hours * 3600)
            
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Game("with life"))
    print(f"We have logged in as {bot.user}")
    bot.loop.create_task(cycle_weather(3))
    try:
        synced=await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)!")
    except:
        print(Exception)
        