import os
from discord.ext import commands
from discord import File
from discord import app_commands
from discord.ui import Button, View, button
import aiosqlite
import random
import datetime
import requests
import time
import os
import sys
import random
import asyncio
import datetime
import json
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from waitress import serve
from math import sqrt
from classlist import *


sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()
token=os.getenv("TOKEN")
intents = discord.Intents.default()
# Only turn on what you actually need:
intents.message_content = True   # True only if you read normal messages
intents.members = False           # True only if you access member lists
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)
app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  serve(app, host='0.0.0.0', port=8080)

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

weathernotifications = {
  "clear": "The sky is clear and calm.",
  "rain": "It is raining steadily.",
  "thunderstorm": "A thunderstorm rages with lightning and thunder.",
  "drought": "A severe drought is affecting the area.",
  "flooding": "Rising water is flooding the surroundings!",
  "sandstorm": "A sandstorm is blowing fiercely across the desert.",
  "haboob": "A massive dust wall, called a haboob, sweeps the desert.",
  "snow": "Snowflakes are falling gently from the sky.",
  "blizzard": "A blizzard is raging, reducing visibility and making travel dangerous.",
  "fog": "Thick fog reduces visibility.",
  "hurricane": "A hurricane is battering the region with strong winds and rain.",
  "typhoon": "A typhoon is approaching, bringing severe winds and rain.",
  "tsunami": "A massive tsunami is approaching from the sea!",
  "avalanche": "An avalanche rushes down the mountain slope!",
  "lava_glow": "Lava glows intensely from volcanic activity.",
  "eruption": "The volcano is erupting violently!",
  "ashfall": "Volcanic ash is falling from the sky.",
  "smoke": "Smoke from volcanic activity fills the air.",
  "calm": "The deep sea is calm and still.",
  "darkness": "The deep sea is dark and eerie.",
  "damp": "The cave is damp and cool.",
  "dry": "The cave is dry and quiet.",
  "icequake": "The ice shifts violently, causing tremors in the frozen ocean.",
  "overcast": "The sky is overcast with clouds."
}

weather_emojis = {
    "clear": "☀️",
    "rain": "🌧️",
    "thunderstorm": "⛈️",
    "drought": "🔥",
    "flooding": "🌊",
    "sandstorm": "🌪️",
    "haboob": "💨",
    "snow": "❄️",
    "blizzard": "🌨️",
    "fog": "🌫️",
    "hurricane": "🌀",
    "typhoon": "🌀",
    "tsunami": "🌊",
    "avalanche": "🏔️",
    "lava_glow": "🌋",
    "eruption": "🌋",
    "ashfall": "🌋",
    "smoke": "💨",
    "calm": "🌊",
    "currents": "🌊",
    "darkness": "🌑",
    "damp": "💧",
    "dry": "🌵",
    "icequake": "🧊",
    "overcast": "☁️"
}

# Optional: map colors to weather types
weather_colors = {
    "clear": discord.Color.blue(),
    "rain": discord.Color.dark_blue(),
    "thunderstorm": discord.Color.dark_purple(),
    "drought": discord.Color.orange(),
    "flooding": discord.Color.teal(),
    "sandstorm": discord.Color.gold(),
    "haboob": discord.Color.dark_gold(),
    "snow": discord.Color.light_grey(),
    "blizzard": discord.Color.greyple(),
    "fog": discord.Color.light_grey(),
    "hurricane": discord.Color.dark_teal(),
    "typhoon": discord.Color.dark_teal(),
    "tsunami": discord.Color.teal(),
    "avalanche": discord.Color.greyple(),
    "lava_glow": discord.Color.red(),
    "eruption": discord.Color.red(),
    "ashfall": discord.Color.dark_grey(),
    "smoke": discord.Color.dark_grey(),
    "calm": discord.Color.blue(),
    "currents": discord.Color.dark_blue(),
    "darkness": discord.Color.dark_grey(),
    "damp": discord.Color.teal(),
    "dry": discord.Color.gold(),
    "icequake": discord.Color.light_grey(),
    "overcast": discord.Color.greyple()
}

if __name__ == "__main__":
    run()
        