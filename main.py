from importlist import *
from classlist import *
@bot.tree.command(name="start", description="Starts the game.")
async def start(ctx: discord.Interaction):
    async with aiosqlite.connect("playerdata.db") as db:
        # Check if this user already has a table
        async with db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (str(ctx.user.id),)
        ) as cursor:
            row = await cursor.fetchone()
        if row:
            await ctx.response.send_message("You already have an account!")
            return
        # Create table for this user
        await db.execute(f"""
            CREATE TABLE IF NOT EXISTS [{ctx.user.id}] (
                balance INTEGER,
                health INTEGER,
                deathcount INTEGER,
                location TEXT,
                inventory TEXT,
                creationdate TEXT,
                winstreak INTEGER,
                highstreak INTEGER,
                badges TEXT
            )
        """)
        # Insert starting data
        clk = datetime.datetime.now()
        ca = clk.strftime("%Y-%m-%d %H:%M:%S")
        await db.execute(f"""
            INSERT INTO [{ctx.user.id}] VALUES (
                1000,        -- balance
                100,         -- health
                0,           -- deathcount
                "Urban",      -- location
                "[]",        -- inventory
                ?,           -- creation date
                0,           -- winstreak
                0,           -- highstreak
                "None"       -- badges
            )
        """, (ca,))
        # Save changes
        await db.commit()
        await ctx.response.send_message("✅ Account created successfully!")

@bot.tree.command(name="profile", description="View your player stats.")
async def profile(ctx: discord.Interaction):
    async with aiosqlite.connect("playerdata.db") as db:
        # Check if the user has a table
        async with db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (str(ctx.user.id),)
        ) as cursor:
            row = await cursor.fetchone()

        if not row:
            await ctx.response.send_message("❌ You don’t have an account yet! Use `/start` first.")
            return

        # Fetch player stats
        async with db.execute(f"SELECT * FROM [{ctx.user.id}]") as cursor:
            stats = await cursor.fetchone()

        if not stats:
            await ctx.response.send_message("⚠️ Could not load your profile data.")
            return

        balance, health, deathcount, location, inventory, creationdate, winstreak, highstreak, badges = stats

        # Create an embed
        embed = discord.Embed(
            title=f"{ctx.user.display_name}'s Profile",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=ctx.user.display_avatar.url)

        embed.add_field(name="Balance", value=str(balance), inline=True)
        embed.add_field(name="Health", value=str(health), inline=True)
        embed.add_field(name="Deaths", value=str(deathcount), inline=True)
        embed.add_field(name="Location", value=str(location), inline=True)
        embed.add_field(name="Created", value=creationdate, inline=False)
        embed.add_field(name="Win Streak", value=str(winstreak), inline=True)
        embed.add_field(name="Highest Streak", value=str(highstreak), inline=True)
        embed.add_field(name="Badges", value=badges, inline=False)

        await ctx.response.send_message(embed=embed)
        
def get_weather(biome: str) -> str:
    # open the weather.json file (where all biome weather is stored)
    with open(WEATHER_FILE, "r") as f:
        data = json.load(f)   # load JSON into a Python dict

    # return the "current" weather value for the biome you asked for
    return data[biome]["current"]

@bot.tree.command(name="weather", description="Check the weather in a biome")
async def weather_command(interaction: discord.Interaction, biome: str=None):
    if biome is None:
        async with aiosqlite.connect("playerdata.db") as db:
            async with db.execute(f"SELECT location FROM '{interaction.user.id}'") as cursor:
                loc_row = await cursor.fetchone()
                biome = loc_row[0]
                current = get_weather(biome.title())
    else:            
        current = get_weather(biome.title())
    emoji = weather_emojis.get(current, "")
    color = weather_colors.get(current, discord.Color.blue())

    # Build the embed
    weather = discord.Embed(
        title=f"Weather update in {biome.title()}",
        description=f"{emoji} **Current Weather:** **{current.title()}**\n\n{weathernotifications.get(current, '')}",
        color=color
    )
    weather.set_footer(text="Weather changes every 3 hours.")
    await interaction.response.send_message(embed=weather)

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
@bot.tree.command(name="anidex", description="Shows animal details.")
async def anidex(interaction: discord.Interaction, name: str):
    await interaction.response.defer()  # avoid timeout

    async with aiosqlite.connect("Organisms.db") as db:
        async with db.execute("SELECT * FROM Animals WHERE name LIKE ?", ('%' + name + '%',)) as cursor:
            row = await cursor.fetchone()

            if row is None:
                await interaction.followup.send(f"❌ No animal found with name **{name}**.")
                return

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
            total_stats = animal.health + animal.attack + animal.defense + animal.speed
            clr=await rarity_color(animal.rarity)
            clr=int(clr, 16)
            embed = discord.Embed(
                title=f"{animal.name} (*{animal.scientific_name}*)",
                description=animal.description or "No description available.",
                color=clr
            )
            embed.add_field(name="Habitat:", value=animal.habitat, inline=True)
            embed.add_field(name="Category:", value=animal.catagory, inline=True)
            embed.add_field(name="Rarity:", value=animal.rarity, inline=True)
            embed.add_field(name=f"Stats: {total_stats}", value=f"Health: {animal.health}\nAttack: {animal.attack}\nDefense: {animal.defense}\nSpeed: {animal.speed}\n", inline=True)
            embed.add_field(name="Ability:", value=animal.ability, inline=False)
            embed.add_field(name="Drops:", value=animal.drops or "None", inline=False)

            if animal.sprite:
                embed.set_image(url=animal.sprite)

            await interaction.followup.send(embed=embed)
            
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

@bot.tree.command(name="encounter", description="Starts a new wilderness encounter.")
async def encounter(interaction: discord.Interaction):
    """A command to initiate a new encounter."""
    await interaction.response.defer()  # Acknowledge immediately
    async with aiosqlite.connect("playerdata.db") as db:
        # Check if the user has a table
        async with db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (str(interaction.user.id),)
        ) as cursor:
            row = await cursor.fetchone()

        if not row:
            await interaction.followup.send("❌ You don’t have an account yet! Use `/start` first.")
            return

        # Fetch player data
        async with db.execute(f"SELECT * FROM [{interaction.user.id}]") as cursor:
            stats = await cursor.fetchone()

        if not stats:
            await interaction.followup.send("⚠️ Could not load your profile data.")
            return

        balance, health, deathcount, location_name, inventory, creationdate, winstreak, highstreak, badges = stats
        p = Player(name=interaction.user.display_name, location=location_name, inventory=inventory)
    # Get a random location (async)
    location = await get_location(p.location)
    if not location:
        await interaction.followup.send("Could not generate a location. Please check the `earth.db` file.")
        return

    # Get animals from the location's biome (async)
    animals_in_biome = await get_animals_by_biome(location.biome)
    if not animals_in_biome:
        await interaction.followup.send(f"An encounter begins in **{location.biome}**... but no animals were found here!")
        return

    # Select an animal based on rarity
    spawned_animal = select_animal_by_rarity(animals_in_biome)
    if not spawned_animal:
        await interaction.followup.send(f"An encounter begins in **{location.biome}**... but something went wrong while spawning an animal.")
        return

    # Create an embed to display the encounter
    clr=await rarity_color(spawned_animal.rarity)
    clr=int(clr, 16)
    embed = discord.Embed(
        title=f"A {(spawned_animal.name).title()} Appeared!",
        description=f"You were searching in {location.biome} area!",
        color=clr
    )

    embed.set_image(url=spawned_animal.sprite)
    embed.add_field(name="Scientific Name", value=f"*{spawned_animal.scientific_name}*", inline=True)
    embed.add_field(name="Description", value=spawned_animal.description, inline=False)

    await interaction.followup.send(embed=embed)
    
import discord
from discord import app_commands
import aiosqlite

@bot.tree.command(name="setlocation", description="Change your current location.")
@app_commands.describe(location="Enter the name of the new location.")
async def setlocation(interaction: discord.Interaction, location: str):
    await interaction.response.defer()  # Acknowledge immediately

    # Check if location exists in your biomes table
    async with aiosqlite.connect("earth.db") as db:
        async with db.execute("SELECT * FROM biomes WHERE name LIKE ?", ('%' + location + '%',)) as cursor:
            loc_row = await cursor.fetchone()

        if loc_row is None:
            await interaction.followup.send(f"❌ The location **{location}** does not exist in the world database.")
            return

        # Update user's location in playerdata.db
        async with aiosqlite.connect("playerdata.db") as player_db:
            # Table is named after the user ID
            await player_db.execute(
                f"UPDATE [{interaction.user.id}] SET location = ?",
                (loc_row[0],)
            )
            await player_db.commit()

    # Create an embed for the new location
    embed = discord.Embed(
        title=f"🌍 You moved to {loc_row[0]}!",
        description=f"Enjoy your adventure!",
        color=discord.Color.green()
    )
    if loc_row[3]:  # biome image
        embed.set_image(url=loc_row[3])

    embed.set_footer(text="Explore and encounter creatures here!")

    await interaction.followup.send(embed=embed)
    
class EncounterPaginator(discord.ui.View):
    def __init__(self, interaction, animals, page_size=10):
        super().__init__(timeout=300)
        self.interaction = interaction
        self.animals = animals
        self.page_size = page_size
        self.current_page = 0
        self.max_page = math.ceil(len(animals) / page_size) - 1

        # Disable prev button on first page
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.max_page

    async def update_embed(self):
        start = self.current_page * self.page_size
        end = start + self.page_size
        embed = discord.Embed(
            title=f"Possible Encounters (Page {self.current_page+1}/{self.max_page+1})",
            color=discord.Color.orange()
        )
        for animal in self.animals[start:end]:
            embed.add_field(
                name=f"{animal.name} ({animal.rarity})",
                value=f"Ability: {animal.ability}",
                inline=False
            )
        await self.message.edit(embed=embed, view=self)

    @discord.ui.button(label="⬅️ Prev", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.prev_button.disabled = self.current_page == 0
            self.next_button.disabled = False

            start = self.current_page * self.page_size
            end = start + self.page_size
            embed = discord.Embed(
                title=f"Possible Encounters (Page {self.current_page+1}/{self.max_page+1})",
                color=discord.Color.orange()
            )
            for animal in self.animals[start:end]:
                embed.add_field(
                    name=f"{animal.name} ({animal.rarity})",
                    value=f"Ability: {animal.ability}",
                    inline=False
                )
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next ➡️", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.max_page:
            self.current_page += 1
            self.next_button.disabled = self.current_page == self.max_page
            self.prev_button.disabled = False

            start = self.current_page * self.page_size
            end = start + self.page_size
            embed = discord.Embed(
                title=f"Possible Encounters (Page {self.current_page+1}/{self.max_page+1})",
                color=discord.Color.orange()
            )
            for animal in self.animals[start:end]:
                embed.add_field(
                    name=f"{animal.name} ({animal.rarity})",
                    value=f"Ability: {animal.ability}",
                    inline=False
                )
            await interaction.response.edit_message(embed=embed, view=self)
            
@bot.tree.command(name="spawnlist", description="Show all possible encounters in your current biome.")
async def spawnlist(interaction: discord.Interaction):
    await interaction.response.defer()

    # Get player's current location
    async with aiosqlite.connect("playerdata.db") as db:
        async with db.execute(f"SELECT location FROM [{interaction.user.id}]") as cursor:
            row = await cursor.fetchone()
            if not row or not row[0]:
                await interaction.followup.send("❌ You don’t have a location set yet. Use `/setlocation` first.")
                return
            current_location = row[0]

    # Get biome of the location
    async with aiosqlite.connect("earth.db") as db:
        async with db.execute("SELECT name FROM biomes WHERE name = ?", (current_location,)) as cursor:
            loc_row = await cursor.fetchone()
            if not loc_row:
                await interaction.followup.send(f"❌ Location `{current_location}` not found in biomes database.")
                return
            biome = loc_row[0]

    # Get animals in this biome
    animals = []
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

    if not animals:
        await interaction.followup.send(f"No animals found in biome `{biome}`.")
        return

    # Send first page
    paginator = EncounterPaginator(interaction, animals)
    embed = discord.Embed(
        title=f"Possible Encounters (Page 1/{paginator.max_page+1})",
        color=discord.Color.orange()
    )
    for animal in animals[:10]:
        embed.add_field(
            name=f"{animal.name} ({animal.rarity})",
            value=f"Ability: {animal.ability}",
            inline=False
        )
    paginator.message = await interaction.followup.send(embed=embed, view=paginator)
    
                        
keep_alive()
bot.run(token)  