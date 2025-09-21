import sqlite3

# Connect to your database
conn = sqlite3.connect("Organisms.db")
cursor = conn.cursor()

# Insert Black Drum
cursor.execute("""
INSERT INTO Animals (
    name, scientific_name, habitat, drops, attack, defense, health, speed,
    abilities, catagory, moves, sprite, rarity, description
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Brown Bullhead Catfish",
    "Ameiurus nebulosus",
    "River, Lake, Swamp",
    "",
    60,
    55,
    90,
    45,
    "Bottom Dweller – Gains defense bonus when resting near riverbeds or in murky water.",
    "Fish",
    "Tail Slam, Fin Crush, Bite, Aqua Dash, Body Slam, Mud Sweep",
    "",
    "Common",
    "A small to medium-sized freshwater catfish native to North America. Brown Bullheads are bottom feeders, eating insects, small fish, and detritus. They are hardy and adapt well to various freshwater environments, including rivers, lakes, and swamps."
))


conn.commit()
conn.close()
