from misc import *

class StarterSelect(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)  # 60 sec timeout
        self.user_id = user_id

    async def give_starter(self, interaction: discord.Interaction, starter):
        # Insert chosen starter into owned.db
        async with aiosqlite.connect("owned.db") as db:
            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS [{self.user_id}] (
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

            await db.execute(f"""
                INSERT INTO [{self.user_id}] 
                (name, nickname, sprite, nature, healthp, attackp, defensep, speedp, moves, training)
                VALUES (?, ?,?, ?, ?, ?, ?, ?, ?,?)
            """, (
                starter["name"],
                starter["nickname"],
                starter["sprite"],
                starter["nature"],
                starter["healthp"],
                starter["attackp"],
                starter["defensep"],
                starter["speedp"],
                starter["moves"],
                starter["training"]
            ))

            await db.commit()

        embed = discord.Embed(
            title=f"🎉 You chose {starter['name']}!",
            description=f"**Nature:** {starter['nature']}\nYour journey begins now!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=starter["sprite"])  # Small preview in corner
        embed.set_image(url=starter["sprite"])      # Big full image
        embed.set_footer(text="Your new companion has joined your adventure!")

        await interaction.response.edit_message(
            content=None,
            embed=embed,
            view=None
        )

    # --- Button callbacks ---
    @discord.ui.button(label="Calico Cat", style=discord.ButtonStyle.primary)
    async def calico(self, interaction: discord.Interaction, button: discord.ui.Button):
        starter = {
            "name": "Calico Cat",
            "nickname": "Calico Cat",
            "sprite": "https://i.postimg.cc/kgZHx9N0/calico.png",
            "nature": "Playful",
            "healthp": 0,
            "attackp": 0,
            "defensep": 0,
            "speedp": 0,
            "moves": json.dumps(["Scratch", "Pounce", "Quick Dash", "Tail Whip"]),
            "training": 0
        }
        await self.give_starter(interaction, starter)

    @discord.ui.button(label="Tuxedo Cat", style=discord.ButtonStyle.success)
    async def tuxedo(self, interaction: discord.Interaction, button: discord.ui.Button):
        starter = {
            "name": "Tuxedo Cat",
            "nickname": "Tuxedo Cat",
            "sprite": "https://i.postimg.cc/8ztCG1zL/tuxedo.png",
            "nature": "Curious",
            "healthp": 0,
            "attackp": 0,
            "defensep": 0,
            "speedp": 0,
            "moves": json.dumps(["Scratch", "Pounce", "Sneaky Dash", "Tail Whip"]),
            "training": 0
        }
        await self.give_starter(interaction, starter)

    @discord.ui.button(label="Tabby Cat", style=discord.ButtonStyle.danger)
    async def tabby(self, interaction: discord.Interaction, button: discord.ui.Button):
        starter = {
            "name": "Tabby Cat",
            "nickname": "Tabby Cat",
            "sprite": "https://i.postimg.cc/rmR3f9HK/tabby.png",
            "nature": "Bold",
            "healthp": 0,
            "attackp": 0,
            "defensep": 0,
            "speedp": 0,
            "moves": json.dumps(["Scratch", "Leap Strike", "Dark Pounce", "Tail Whip"]),
            "training": 0
        }
        await self.give_starter(interaction, starter)
        
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
    view = StarterSelect(ctx.user.id)
    await ctx.response.send_message(
        "🎉 Account created! Choose your starter cat:",
        view=view
    )

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
          

class EncounterView(View):
    def __init__(self, spawned_animal, player):
        super().__init__(timeout=60)
        self.spawned_animal = spawned_animal
        self.player = player

    @button(label="⚔️ Fight", style=discord.ButtonStyle.red)
    async def fight_button(self, interaction: discord.Interaction, button: Button):
        winner = await battle(self.player, self.spawned_animal,"wild")
        if winner == self.player.id:
            # After win → show Capture & Loot options
            new_view = CaptureLootView(self.spawned_animal, self.player)
            await interaction.response.edit_message(
                embed=interaction.message.embeds[0],
                content=f"⚔️ You defeated **{self.spawned_animal.name}**!\nWhat do you want to do?",
                view=new_view
            )
        else:
            await interaction.response.edit_message(
                content=f"💀 You were defeated by **{self.spawned_animal.name}**...",
                view=None
            )

    @button(label="🏃 Run", style=discord.ButtonStyle.gray)
    async def run_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(
            content="🏃 You escaped safely!",
            view=None
        )


class CaptureLootView(View):
    def __init__(self, spawned_animal, player):
        super().__init__(timeout=30)
        self.spawned_animal = spawned_animal
        self.player = player

    @button(label="🎯 Capture", style=discord.ButtonStyle.green)
    async def capture_button(self, interaction: discord.Interaction, button: Button):
        await save_capture(self.player, self.spawned_animal)  # <-- DB save function
        await interaction.response.edit_message(
            content=f"🎉 You captured **{self.spawned_animal.name}**!",
            view=None
        )

    @button(label="💰 Loot", style=discord.ButtonStyle.blurple)
    async def loot_button(self, interaction: discord.Interaction, button: Button):
        loot_item = random.choice(self.spawned_animal.drop.split(',')) # <-- generate item(s)
        await add_to_inventory(self.player, loot_item)   # <-- save in DB
        await interaction.response.edit_message(
            content=f"💰 You looted **{loot_item}** from {self.spawned_animal.name}!",
            view=None
        )
        
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
        p = Player(name=interaction.user.display_name, location=location_name, inventory=inventory,idt=interaction.user.id)
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
    spawned_animal.healthp=random.randint(-50,50)
    spawned_animal.attackp=random.randint(-50,50)
    spawned_animal.defensep=random.randint(-50,50)
    spawned_animal.speedp=random.randint(-50,50)
    mh=await calc_stat(spawned_animal.health,spawned_animal.healthp)
    ma=await calc_stat(spawned_animal.attack,spawned_animal.attackp)
    md=await calc_stat(spawned_animal.defense,spawned_animal.defensep)
    ms=await calc_stat(spawned_animal.speed,spawned_animal.speedp)
    embed = discord.Embed(
        title=f"{(spawned_animal.name).title()} Appeared!",
        description=f"You were searching in {location.biome}!",
        color=clr
    )

    embed.set_image(url=spawned_animal.sprite)
    embed.add_field(name="Scientific Name", value=f"*{spawned_animal.scientific_name}*", inline=True)
    embed.add_field(name="Description", value=spawned_animal.description, inline=False)
    embed.add_field(name="Stats", value=f"HP: {mh}\nAttack: {ma}\nDefense: {md}\nSpeed: {ms}", inline=True)
    embed.set_footer(text=f"Location: {location_name} | Keep exploring!")
    view = EncounterView(spawned_animal, p)
    await interaction.followup.send(embed=embed, view=view)

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

class AnimalInfoView(discord.ui.View):
    def __init__(self, animals, start_index=0):
        super().__init__(timeout=60)
        self.animals = animals
        self.index = start_index
        self.update_buttons()

    def update_buttons(self):
        self.prev_button.disabled = self.index <= 0
        self.next_button.disabled = self.index >= len(self.animals) - 1

    def get_embed(self):
        animal = self.animals[self.index]
        embed = discord.Embed(
            title=f"📖 Animal Info ({self.index+1}/{len(self.animals)})",
            description=f"**Name:** {animal['name']}\n"
                        f"**Nickname:** {animal['nickname']}\n"
                        f"**Nature:** {animal['nature']}\n"
                        f"**HP:** {animal['healthp']}\n"
                        f"**Attack:** {animal['attackp']}\n"
                        f"**Defense:** {animal['defensep']}\n"
                        f"**Speed:** {animal['speedp']}\n"
                        f"**Moves:** {animal['moves']}\n"
                        f"**Training:** {animal['training']}",
            color=discord.Color.green()
        )
        if animal['sprite']:
            embed.set_thumbnail(url=animal['sprite'])
        return embed

    @discord.ui.button(label="⬅ Previous", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Next ➡", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)


# Slash command version
@bot.tree.command(name="animals", description="View your captured animals")
@app_commands.describe(index="The number of the animal in your collection (optional)")
async def animals(interaction: discord.Interaction, index: int = 1):  # default = 1 (first animal)
    table_name = str(interaction.user.id)

    async with aiosqlite.connect("owned.db") as db:
        cursor = await db.execute(f"""
            SELECT name, nickname, sprite, nature, healthp, attackp, defensep, speedp, moves, training
            FROM [{table_name}]
        """)
        rows = await cursor.fetchall()

    if not rows:
        await interaction.response.send_message("❌ You don’t own any animals yet!", ephemeral=True)
        return

    animals = [
        {
            "name": row[0],
            "nickname": row[1],
            "sprite": row[2],
            "nature": row[3],
            "healthp": row[4],
            "attackp": row[5],
            "defensep": row[6],
            "speedp": row[7],
            "moves": row[8],
            "training": row[9]
        }
        for row in rows
    ]

    # clamp index to valid range
    start_index = max(0, min(index - 1, len(animals) - 1))

    view = AnimalInfoView(animals, start_index=start_index)
    await interaction.response.send_message(embed=view.get_embed(), view=view) 
                        
keep_alive()
bot.run(token)  