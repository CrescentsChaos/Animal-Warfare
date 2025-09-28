from importlist import *
from moves import *

async def get_weather(biome: str) -> str:
    # open the weather.json file (where all biome weather is stored)
    with open('weather.json', "r") as f:
        data = json.load(f)   # load JSON into a Python dict
        
    # return the "current" weather value for the biome you asked for
    return data[biome]["current"]
async def hpbar(attacker):
    healthbar = "<:HP:1107296292243255356>" + "<:GREY:1107331848360689747>" * 10 + "<:END:1107296362988580907>"
    if True:
        if 0.6 < (attacker.health / attacker.maxhealth) <= 1:
            healthbar = "<:health:1107296292243255356>" + "<:GREEN:1107296335780139113>" * int((attacker.health / attacker.maxhealth) * 10) + "<:GREY:1107331848360689747>" * (10 - int((attacker.health / attacker.maxhealth) * 10)) + "<:END:1107296362988580907>"
        elif 0.3 < (attacker.health / attacker.maxhealth) <= 0.6:
            healthbar = "<:health:1107296292243255356>" + "<:YELLOW:1107331825929556111>" * int((attacker.health / attacker.maxhealth) * 10) + "<:GREY:1107331848360689747>" * (10 - int((attacker.health / attacker.maxhealth) * 10)) + "<:END:1107296362988580907>"
        elif 0 < (attacker.health / attacker.maxhealth) <= 0.3:
            healthbar = "<:health:1107296292243255356>" + "<:RED:1107331787480379543>" * int((attacker.health / attacker.maxhealth) * 10) + "<:GREY:1107331848360689747>" * (10 - int((attacker.health / attacker.maxhealth) * 10)) + "<:END:1107296362988580907>"
    return healthbar

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
                wt=await get_weather(row[0])
                if row:
                    location = Location(
                        biome=row[0],
                        weather=wt,
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
                naturelist=["Playful","Aggressive","Brutal","Ferocious","Resilient","Hardy","Durable","Stalwart","Guarded","Solid","Swift","Agile","Nimble"]
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
                        category=row[9],
                        drops=row[3],
                        sprite=row[11],
                        description=row[13],
                        moves=row[10],
                        nature=random.choice(naturelist)
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
                ability TEXT,
                healthp INTEGER,
                attackp INTEGER,
                defensep INTEGER,
                speedp INTEGER,
                moves TEXT,
                training INTEGER
            )
        """)
        new=animal.moves.split(",")
        mod_move = await get_moves(new)
        # Insert animal data
        await db.execute(f"""
            INSERT INTO [{table_name}] 
            (name,nickname,
            sprite, nature, ability,
             healthp, attackp, defensep, speedp, moves,training)
            VALUES (?, ?,?, ?, ?, ?, ?, ?, ?, ?,?)
        """, (
            animal.name,
            animal.name,
            animal.sprite,
            animal.nature,
            animal.ability,
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

            
async def convert_allyanimal(user_id: int) -> BattleAnimal | None:
    # 1️⃣ Get companion ID from playerdata.db
    async with aiosqlite.connect("playerdata.db") as db:
        cursor = await db.execute(f"SELECT companion FROM [{user_id}]")
        row = await cursor.fetchone()
        if not row:
            return None
        companion_id = row[0]
    # 2️⃣ Get companion data from owned.db
    async with aiosqlite.connect("owned.db") as db:
        cursor = await db.execute(f"""
            SELECT name, sprite, ability, nature, moves, healthp, attackp, defensep, speedp
            FROM [{user_id}]
            WHERE id = ?
        """, (companion_id,))
        row = await cursor.fetchone()
        if not row:
            return None

        name, sprite, ability, nature, moves_json, healthp, attackp, defensep, speedp = row
        moves = json.loads(moves_json)
    async with aiosqlite.connect("Organisms.db") as db:
        cursor = await db.execute(f"""
            SELECT health, attack, defense, speed, category
            FROM Animals
            WHERE name = ?
        """, (name,))
        animalstat = await cursor.fetchone()
    # 3️⃣ Create BattleAnimal
    # Here 'drop' can be empty or fetched later
    battle_animal = BattleAnimal(
        name=name,
        sprite=sprite,  # You can customize later
        ability=ability,
        category=animalstat[4],  # You can customize later
        nature=nature,
        moves=moves,
        drop=None,   # You can customize later
        health=await calc_stat(animalstat[0],healthp),
        attack=await calc_stat(animalstat[1],attackp),
        defense=await calc_stat(animalstat[2],defensep),
        speed=await calc_stat(animalstat[3],speedp)
    )

    return battle_animal
       
async def convert_wildanimal(animal):
    async with aiosqlite.connect("Organisms.db") as db:
        async with db.execute("SELECT * FROM Animals WHERE name = ?", (animal.name,)) as cursor:
            row = await cursor.fetchone()
            naturelist=["Playful","Aggressive","Brutal","Ferocious","Resilient","Hardy","Durable","Stalwart","Guarded","Solid","Swift","Agile","Nimble"]
            if row:
                battle_animal = BattleAnimal(
                    name=animal.name,
                    sprite=animal.sprite,
                    ability=animal.ability,
                    category=animal.category,
                    nature=random.choice(naturelist),
                    moves=await get_moves(row[10].split(",")),
                    drop=random.choice(animal.drops.split(",")),
                    health=await calc_stat(animal.health,animal.healthp),
                    attack=await calc_stat(animal.attack,animal.attackp),
                    defense=await calc_stat(animal.defense,animal.defensep),
                    speed=await calc_stat(animal.speed,animal.speedp)
                )
                battle_animal= await apply_nature(battle_animal)
                return battle_animal
            
async def apply_nature(animal):
    NATURES = {
    "Aggressive":   {"up": "attack", "down": "defense"},
    "Brutal":       {"up": "attack", "down": "speed"},
    "Ferocious":    {"up": "attack", "down": "health"},
    "Resilient":    {"up": "health", "down": "speed"},
    "Hardy":        {"up": "health", "down": "attack"},
    "Durable":      {"up": "health", "down": "defense"},
    "Stalwart":     {"up": "defense", "down": "speed"},
    "Guarded":      {"up": "defense", "down": "attack"},
    "Solid":        {"up": "defense", "down": "health"},
    "Swift":        {"up": "speed", "down": "health"},
    "Agile":        {"up": "speed", "down": "defense"},
    "Nimble":       {"up": "speed", "down": "attack"},
    # Neutral options
    "Playful":     {"up": None, "down": None}
}
    """Applies a random nature effect to an animal object with stats."""
    nature = random.choice(list(NATURES.keys()))
    effect = NATURES[nature]

    # Save nature to the animal
    animal.nature = nature  

    if effect["up"] and effect["down"]:  
        # Increase one stat by 10%, decrease another by 10%
        up_attr = effect["up"]
        down_attr = effect["down"]

        # Apply boost
        setattr(animal, up_attr, int(getattr(animal, up_attr) * 1.1))
        # Apply reduction (at least 1)
        setattr(animal, down_attr, max(1, int(getattr(animal, down_attr) * 0.9)))
    animal.maxhealth=animal.health
    return animal
async def fetch_animal(name):
    async with aiosqlite.connect("Organisms.db") as db:
        cursor = await db.execute("SELECT * FROM Animals where name==?",(name,))
        row = await cursor.fetchone()
    naturelist=["Playful","Aggressive","Brutal","Ferocious","Resilient","Hardy","Durable","Stalwart","Guarded","Solid","Swift","Agile","Nimble"]
    animal = Animal(
            name=row[0],
            scientific_name=row[1],
            habitat=row[2],
            drops=row[3],
            attack=row[4],
            defense=row[5],
            health=row[6],
            speed=row[7],
            ability=row[8],
            category=row[9],
            moves=row[10],
            sprite=row[11],
            rarity=row[12],
            description=row[13],
            nature=random.choice(name)
        )

    return animal 
    
async def get_animal_name(user_id: int, animal_id: int) -> str | None:
    """
    Fetch an animal's nickname (if set) or name from owned.db.
    Returns None if the animal doesn't exist.
    """
    async with aiosqlite.connect("owned.db") as db:
        await db.execute(f"""
            CREATE TABLE IF NOT EXISTS [{user_id}] (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                nickname TEXT,
                sprite TEXT,
                nature TEXT,
                ability TEXT,
                healthp INTEGER,
                attackp INTEGER,
                defensep INTEGER,
                speedp INTEGER,
                moves TEXT,
                training INTEGER
            )
        """)
        await db.commit()

        cursor = await db.execute(f"SELECT name, nickname FROM [{user_id}] WHERE id = ?", (animal_id,))
        result = await cursor.fetchone()

    if not result:
        return None  # No such animal owned by player

    name, nickname = result
    return nickname if nickname else name   
async def environmenteff(animal1,animal2,field,embed):
    if not field.effects:
        return
    elif field.effects:
        field.effects=False
    if field.weather.title()=="Thunderstorm":
        if "Flying" in animal1.category:
            animal1.speed*=0.75
            embed.add_field(name="Disadvantage!",value=f"Thunderstorm is halting {animal1.name}'s speed.",inline=False)
        if "Flying" in animal2.category:
            animal2.speed*=0.75
            embed.add_field(name="Disadvantage!",value=f"Thunderstorm is halting {animal2.name}'s speed.",inline=False)
    if field.biome in ["Ocean","River","Frozen Ocean"]:
        if "Aquatic" not in animal1.category and "Flying" not in animal1.category:
            animal1.status.append("Drown") 
            embed.add_field(name="Disadvantage!",value=f"{animal1.name} is drowning.",inline=False)  
        if "Aquatic" not in animal2.category and "Flying" not in animal2.category:
            animal2.status.append("Drown") 
            embed.add_field(name="Disadvantage!",value=f"{animal2.name} is drowning.",inline=False) 

async def statuscheck(attacker,defender,move,player,foe,field,embed):
    if "Drown" in attacker.status:
        attacker.oxygen-=20  
        embed.add_field(name="Drowning!",value=f"{attacker.name}'s oxygen is depleting.",inline=False)  
    if "Drown" in attacker.status and attacker.oxygen<=0:
        attacker.health=0
        embed.add_field(name="Drowned!",value=f"{attacker.name}'s drowned completely.",inline=False)
                      
async def attack(attacker,defender,move,player,foe,field,embed):
    await staminacost(attacker,20,embed)
    attacks={
        "Tackle" : tackle,
        "Scratch" : scratch,
        "Bite" : bite,
        "Peck" : peck,
        "Pounce" : pounce,
        "Tail Whip" : tailwhip,
        "Electricution": electricution,
        "Gore": gore,
        "Suction": suction,
        "Death Roll": deathroll,
        "Piercing Beak": piercingbeak,
        "Venomous Fang": venomousfang,
        "Fin Slash": finslash,
        "Predatory Surge": predatorysurge,
        "Dash" : dash,
        "Leap" : leap,
        "Dig" : dig
    }
    if move in attacks and "Flinch" not in attacker.status:
        await attacks[move](attacker,defender,move,player,foe,field,embed)
    if "Flinch" in attacker.status:
        attacker.status.remove("Flinch")
        
      
    
    