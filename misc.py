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
                        moves=row[10],
                        nature=random.choice(["Brave","Calm","Timid","Jolly","Modest","Bold","Hasty","Quiet","Sassy","Adamant"])
                    )
                    animals.append(animal)
                    
        return animals
    except Exception as e:
        print(f"Database error (get_animals_by_biome): {e}")
        return []

async def calc_stat(base,potential):
    modified=(base+(1+(base*0.1)*(potential*0.02)))*2
    return round(modified)

async def decide_turn(ally,foe):
    if ally.speed>foe.speed:
        return ally,foe
    elif foe.speed>ally.speed:
        return foe,ally
    else:
        return random.choice([(ally,foe),(foe,ally)])
    
async def save_capture(player, animal):
    """
    Saves a captured animal into owned.db under the player's table.
    """
    table_name = str(player.id)  # use Discord user ID as table name

    async with aiosqlite.connect("owned.db") as db:
        # Create user table if it doesn't exist
        await db.execute(f"""
            CREATE TABLE IF NOT EXISTS [{table_name}] (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                nickname TEXT,
                sprite TEXT,
                nature TEXT,
                healthp INTEGER,
                attackp INTEGER,
                defensep INTEGER,
                speedp INTEGER,
                moves TEXT,
                training INTEGER
            )
        """)
        mod_move = await get_moves(animal.moves.split(","))
        # Insert animal data
        await db.execute(f"""
            INSERT INTO [{table_name}] 
            (name,nickname,
            sprite, nature, 
             healthp, attackp, defensep, speedp, moves,training)
            VALUES (?, ?,?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            animal.name,
            animal.name,
            animal.sprite,
            animal.nature,
            animal.healthp,
            animal.attackp,
            animal.defensep,
            animal.speedp,
            json.dumps(mod_move),  # store moves as JSON
            animal.training
        ))

        await db.commit()
        
async def add_to_inventory(user, item_name, quantity: int = 1):
    """
    Adds an item with quantity to the player's inventory.
    Inventory is stored as JSON inside the player's row.
    """
    async with aiosqlite.connect("playerdata.db") as db:
        # Get current inventory
        async with db.execute(f"SELECT inventory FROM [{user.id}]") as cursor:
            row = await cursor.fetchone()

        if not row:
            return False  # no player data found

        try:
            inventory = json.loads(row[0]) if row[0] else {}
        except json.JSONDecodeError:
            inventory = {}

        # Update inventory
        if item_name in inventory:
            inventory[item_name] += quantity
        else:
            inventory[item_name] = quantity

        # Save back to DB
        await db.execute(
            f"UPDATE [{user.id}] SET inventory = ?",
            (json.dumps(inventory),)
        )
        await db.commit()      
        
async def get_moves(movelist, num=4):
    new=random.sample(movelist, min(num, len(movelist)))
    # Randomly select 'num' unique moves from the movelist
    return new
       
async def convert_wildanimal(animal):
    async with aiosqlite.connect("Organisms.db") as db:
        async with db.execute("SELECT * FROM Animals WHERE name = ?", (animal.name,)) as cursor:
            row = await cursor.fetchone()
            if row:
                battle_animal = BattleAnimal(
                    name=animal.name,
                    ability=animal.ability,
                    nature=random.choice(["Brave","Calm","Timid","Jolly","Modest","Bold","Hasty","Quiet","Sassy","Adamant"]),
                    moves=await get_moves(row[10]),
                    drop=random.choice(animal.drops.split(",")),
                    health=await calc_stat(animal.health,animal.healthp),
                    attack=await calc_stat(animal.attack,animal.attackp),
                    defense=await calc_stat(animal.defense,animal.defensep),
                    speed=await calc_stat(animal.speed,animal.speedp)
                )
                return battle_animal
        
async def battle(ally,foe,battle_type):
    if battle_type=="wild":
        foe=await convert_wildanimal(foe)
    return ally.id
    