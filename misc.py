from importlist import *

def get_weather(biome: str) -> str:
    # open the weather.json file (where all biome weather is stored)
    with open(WEATHER_FILE, "r") as f:
        data = json.load(f)   # load JSON into a Python dict

    # return the "current" weather value for the biome you asked for
    return data[biome]["current"]

def select_animal_by_rarity(animals):
    """Selects a single animal from a list based on its rarity."""
    if not animals:
        return None

    rarity_weights = {
        'Common': 800,
        'Uncommon': 400,
        'Rare': 200,
        'Epic': 100,
        'Legendary': 50,
        'Mythical': 1
    }

    weighted_animals = []
    for animal in animals:
        weight = rarity_weights.get(animal.rarity, 0)
        weighted_animals.extend([animal] * weight)

    if not weighted_animals:
        return None

    return random.choice(weighted_animals)

async def rarity_color(rarity):
    """Returns a discord.Color based on the rarity string."""
    colors = {
        'Common': "0xa1a1a1",
        'Uncommon': "0x05ff58",
        'Rare': "0x008cff",
        'Epic': "0x6200ff",
        'Legendary': "0xff6803",
        'Mythical': "0xff00bf"
    }
    return colors[rarity]

async def get_location(loc):
    """Selects a random location from the earth.db database."""
    try:
        async with aiosqlite.connect("earth.db") as db:
            async with db.execute("SELECT * FROM biomes where name==?",(loc,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    location = Location(
                        biome=row[0],
                        terrain=row[1],
                        time=None,       # leave as None if not in DB
                        disaster=None,   # leave as None if not in DB
                        loot=row[2],      # maybe convert string to list if needed
                        image=row[3]     # image URL or path
                    )
                    return location
        return None
    except Exception as e:
        print(f"Database error (get_random_location): {e}")
        return None
    
async def get_animals_by_biome(biome):
    """Fetches all animals for a given biome from the Organisms.db database."""
    animals = []
    try:
        async with aiosqlite.connect("Organisms.db") as db:
            async with db.execute("SELECT * FROM Animals WHERE habitat LIKE ?", ('%' + biome + '%',)) as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    animal = Animal(
                        name=row[0],
                        scientific_name=row[1],
                        habitat=row[2],
                        ability=row[8],
                        health=row[6],
                        attack=row[4],
                        defense=row[5],
                        speed=row[7],
                        rarity=row[12],
                        catagory=row[9],
                        drops=row[3],
                        sprite=row[11],
                        description=row[13],
                        moves=row[10]
                    )
                    animals.append(animal)
                    
        return animals
    except Exception as e:
        print(f"Database error (get_animals_by_biome): {e}")
        return []