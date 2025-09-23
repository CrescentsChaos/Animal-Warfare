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
                    ability TEXT,
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
                (name, nickname, sprite, nature, ability,healthp, attackp, defensep, speedp, moves, training)
                VALUES (?, ?,?,?, ?, ?, ?, ?, ?, ?,?)
            """, (
                starter["name"],
                starter["nickname"],
                starter["sprite"],
                starter["nature"],
                starter["ability"],
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
            "ability": "Agile",
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
            "nature": "Playful",
            "ability": "Stealthy",
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
            "nature": "Playful",
            "ability": "Strong",
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
                companion INTEGER
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
                1       -- companion
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

        balance, health, deathcount, location, inventory, creationdate, winstreak, highstreak, companionidx = stats

        # Create an embed
        embed = discord.Embed(
            title=f"{ctx.user.display_name}'s Profile",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=ctx.user.display_avatar.url)
        companion=await get_animal_name(ctx.user.id,companionidx)
        embed.add_field(name="Balance", value=str(balance), inline=True)
        embed.add_field(name="Health", value=str(health), inline=True)
        embed.add_field(name="Deaths", value=str(deathcount), inline=True)
        embed.add_field(name="Location", value=str(location), inline=True)
        embed.add_field(name="Created", value=creationdate, inline=False)
        embed.add_field(name="Win Streak", value=str(winstreak), inline=True)
        embed.add_field(name="Highest Streak", value=str(highstreak), inline=True)
        embed.add_field(name="Companion", value=companion, inline=False)

        await ctx.response.send_message(embed=embed)
        

@bot.tree.command(name="weather", description="Check the weather in a biome")
async def weather_command(interaction: discord.Interaction, biome: str=None):
    if biome is None:
        async with aiosqlite.connect("playerdata.db") as db:
            async with db.execute(f"SELECT location FROM '{interaction.user.id}'") as cursor:
                loc_row = await cursor.fetchone()
                biome = loc_row[0]
                current =await get_weather(biome.title())
    else:            
        current =await  get_weather(biome.title())
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
          
class BattleView(View):
    def __init__(self, player, ally, foe, message,spawned_animal):
        super().__init__(timeout=120)
        self.player = player
        self.ally = ally
        self.foe = foe
        self.turn = 1
        self.battle_over = False
        self.message = message  # Store the original battle message
        self.spawned_animal=spawned_animal

        for move in ally.moves:
            self.add_item(self.create_move_button(move))

    def create_move_button(self, move_name):
        button = Button(label=move_name, style=discord.ButtonStyle.green)
        async def callback(interaction: discord.Interaction):
            if self.battle_over:
                await interaction.response.send_message("⚠️ Battle already ended.", ephemeral=True)
                return
            # Acknowledge the interaction to prevent the "Interaction Failed" error
            await interaction.response.defer()
            # The message edit will now be handled inside process_turn after deferring
            await self.process_turn(interaction, move_name)

        button.callback = callback
        return button

    async def process_turn(self, interaction: discord.Interaction, ally_move):
        # Disable buttons immediately
        for item in self.children:
            item.disabled = True

        try:
            # Check if the battle is already over
            if self.battle_over:
                await interaction.response.send_message("The battle has already ended.", ephemeral=True)
                return

            # Your battle logic here...
            weather = await get_weather(self.player.location)
            field = Location(biome=self.player.location, terrain="Normal", time="None", disaster="None", loot="None", image="None")
            
            embed = discord.Embed(
                title=f"⚔️ Turn {self.turn}",
                description=f"",
                color=discord.Color.red()
            )
            
            # Determine turn order based on speed
            if self.ally.speed > self.foe.speed or (self.ally.speed == self.foe.speed and random.choice([True, False])):
                await attack(self.ally, self.foe, ally_move, self.player, self.foe, field, embed)
                if self.foe.health > 0:
                    await attack(self.foe, self.ally, random.choice(self.foe.moves), self.foe, self.player, field, embed)
                
            else:
                await attack(self.foe, self.ally, random.choice(self.foe.moves), self.foe, self.player, field, embed)
                if self.ally.health > 0:
                    await attack(self.ally, self.foe, ally_move, self.player, self.foe, field, embed)
                
                    
                    
            # Update embed fields
            embed.add_field(name=f"{self.ally.name} HP", value=f"{str(max(0, self.ally.health))}/{self.ally.maxhealth}")
            embed.add_field(name=f"{self.foe.name} HP", value=f"{str(max(0, self.foe.health))}/{self.foe.maxhealth}")
            embed.set_thumbnail(url=self.ally.sprite)
            embed.set_image(url=self.spawned_animal.sprite)
            
            # Check for battle end
            if self.ally.health <= 0 or self.foe.health <= 0:
                self.battle_over = True
                await self.end_battle()
                return
            for item in self.children:
                item.disabled = False
            await interaction.message.edit(embed=embed, view=self)  
            
        except Exception as e:
            print(f"Error during battle turn: {e}")
            traceback.print_exc() 
            await self.message.edit(content=f"An unexpected error occurred during the battle. Please try again. Error: `{e}`", view=None)
            
        finally:
            self.turn += 1
            
    async def end_battle(self):
        # Your existing end_battle logic...
        if self.ally.health > 0:
            new_view = CaptureLootView(self.spawned_animal, self.player)
            embed = discord.Embed(
                title=f"🎉 {self.player.name} won!",
                description=f"Your **{self.ally.name}** defeated **{self.foe.name}**! What will you do now?",
                color=discord.Color.green()
            )
            embed.set_image(url=self.foe.sprite)
            await self.message.edit(embed=embed, view=new_view)
        else:
            embed = discord.Embed(
                title=f"💀 Defeated!",
                description=f"Your **{self.ally.name}** was defeated by **{self.foe.name}**!",
                color=discord.Color.dark_red()
            )
            embed.set_image(url=self.ally.sprite)
            await self.message.edit(embed=embed, view=None)

class EncounterView(View):
    def __init__(self, spawned_animal, player):
        super().__init__(timeout=60)
        self.spawned_animal = spawned_animal
        self.player = player

    @button(label="⚔️ Battle", style=discord.ButtonStyle.danger)
    async def fight_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()  # acknowledge interaction

        ally = await convert_allyanimal(self.player.id)
        foe = await convert_wildanimal(self.spawned_animal)

        # Send initial battle message
        battle_embed = discord.Embed(
            title="⚔️ Battle Start!",
            description=f"{ally.name} vs {foe.name}",
            color=discord.Color.orange()
        )  # get the message object
        battle_embed.add_field(name=f"{ally.name} HP", value=f"{str(max(0, ally.health))}/{ally.maxhealth}")
        battle_embed.add_field(name=f"{foe.name} HP", value=f"{str(max(0, foe.health))}/{foe.maxhealth}")
        battle_embed.set_thumbnail(url=ally.sprite)
        battle_embed.set_image(url=self.spawned_animal.sprite)
        # Pass ONLY the message to BattleView
        battle_view = BattleView(self.player, ally, foe, interaction.message,self.spawned_animal)
        await interaction.edit_original_response(embed=battle_embed, view=battle_view)

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
        await interaction.response.defer()
        await save_capture(self.player, self.spawned_animal)  # <-- DB save function
        await interaction.edit_original_response(
            content=f"🎉 You captured **{self.spawned_animal.name}**!",embed=None,
            view=None
        )

    @button(label="💰 Loot", style=discord.ButtonStyle.blurple)
    async def loot_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        loot_item = random.choice(self.spawned_animal.drop.split(',')) # <-- generate item(s)
        await add_to_inventory(self.player, loot_item)   # <-- save in DB
        await interaction.edit_original_response(
            content=f"💰 You looted **{loot_item}** from {self.spawned_animal.name}!",embed=None,
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
    embed = discord.Embed(
        title=f"{(spawned_animal.name).title()} Appeared!",
        description=f"You were searching in {location.biome}!",
        color=clr
    )

    embed.set_image(url=spawned_animal.sprite)
    embed.add_field(name="Scientific Name", value=f"*{spawned_animal.scientific_name}*", inline=False)
    embed.add_field(name="Description", value=spawned_animal.description, inline=False)
    embed.set_footer(text=f"Location: {location_name} | Keep exploring!")
    view = EncounterView(spawned_animal, p)
    msg = await interaction.followup.send(embed=embed, view=view)

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

    async def get_embed(self):
        animal = self.animals[self.index]
        spawned_animal=await fetch_animal(animal['name'])
        mh=await calc_stat(spawned_animal.health,animal['healthp'])
        ma=await calc_stat(spawned_animal.attack,animal['attackp'])
        md=await calc_stat(spawned_animal.defense,animal['defensep'])
        ms=await calc_stat(spawned_animal.speed,animal['speedp'])
        moves = json.loads(animal['moves'])
        embed = discord.Embed(
            title=f"{animal['nickname']}",
            description=f"**Name:** {animal['name']}\n"
                        f"**Scientific Name:** *{spawned_animal.scientific_name}*\n"
                        f"{spawned_animal.description}",
            color=discord.Color.green()
        )
        embed.add_field(name="Nature", value=animal['nature'], inline=True)
        embed.add_field(name="Ability", value=animal['ability'], inline=True)
        embed.add_field(name="Stats", value=f"HP: {mh}\nAttack: {ma}\nDefense: {md}\nSpeed: {ms}", inline=False )
        embed.add_field(name="Moves",value=f"1. {moves[0]}\n2. {moves[1]}\n3. {moves[2]}\n4. {moves[3]}",inline=False)
        embed.set_footer(text=f"Pages: {self.index+1}/{len(self.animals)}")
        if animal['sprite']:
            embed.set_image(url=animal['sprite'])
        return embed

    @discord.ui.button(label="⬅ Previous", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=await self.get_embed(), view=self)

    @discord.ui.button(label="Next ➡", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=await self.get_embed(), view=self)


# Slash command version
@bot.tree.command(name="info", description="View your captured animals")
@app_commands.describe(index="The number of the animal in your collection (optional)")
async def info(interaction: discord.Interaction, index: int = 1):  # default = 1 (first animal)
    table_name = str(interaction.user.id)

    async with aiosqlite.connect("owned.db") as db:
        cursor = await db.execute(f"""
            SELECT name, nickname, sprite, nature, ability,healthp, attackp, defensep, speedp, moves, training
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
            "ability": row[4],  # Assuming ability is stored in nature column
            "healthp": row[5],
            "attackp": row[6],
            "defensep": row[7],
            "speedp": row[8],
            "moves": row[9],
            "training": row[10]
        }
        for row in rows
    ]

    # clamp index to valid range
    start_index = max(0, min(index - 1, len(animals) - 1))

    view = AnimalInfoView(animals, start_index=start_index)
    await interaction.response.send_message(embed=await view.get_embed(), view=view) 
    
class AnimalsListView(View):
    def __init__(self, animals, user_id, page=0, per_page=10):
        super().__init__(timeout=60)
        self.animals = animals
        self.user_id = user_id  # restrict buttons to the user
        self.page = page
        self.per_page = per_page
        self.update_buttons()

    def update_buttons(self):
        # Clear old buttons
        self.clear_items()
        # Add Previous button if not first page
        if self.page > 0:
            prev_button = Button(label="⬅ Previous", style=discord.ButtonStyle.secondary, custom_id="prev")
            prev_button.callback = self.button_callback
            self.add_item(prev_button)
        # Add Next button if not last page
        if (self.page + 1) * self.per_page < len(self.animals):
            next_button = Button(label="Next ➡", style=discord.ButtonStyle.secondary, custom_id="next")
            next_button.callback = self.button_callback
            self.add_item(next_button)

    def get_embed(self):
        start = self.page * self.per_page
        end = start + self.per_page
        page_animals = self.animals[start:end]

        description = ""
        for i, animal in enumerate(page_animals, start=start + 1):
            description += f"**{i}. {animal['nickname']}** ({animal['name']})\n"

        total_pages = (len(self.animals) - 1) // self.per_page + 1
        embed = discord.Embed(
            title=f"📜 Captured Animals (Page {self.page + 1}/{total_pages})",
            description=description,
            color=discord.Color.green()
        )
        return embed

    async def button_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ You cannot control this.", ephemeral=True)
            return

        if interaction.data["custom_id"] == "next":
            self.page += 1
        elif interaction.data["custom_id"] == "prev":
            self.page -= 1

        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
        
#Command: setnickname        
@bot.tree.command(name="setnickname", description="Set a nickname for one of your animals")
@app_commands.describe(animal_id="The ID of the animal you want to rename", nickname="The new nickname")
async def setnickname(interaction: discord.Interaction, animal_id: int, nickname: str):
    user_id = interaction.user.id

    # Ensure the user table exists
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

        # Check if the animal exists
        cursor = await db.execute(f"SELECT name FROM [{user_id}] WHERE id = ?", (animal_id,))
        animal = await cursor.fetchone()

        if not animal:
            await interaction.response.send_message("❌ You don’t own an animal with that ID.", ephemeral=True)
            return

        # Update nickname
        await db.execute(f"UPDATE [{user_id}] SET nickname = ? WHERE id = ?", (nickname, animal_id))
        await db.commit()

    await interaction.response.send_message(
        f"✅ Nickname for **{animal[0]}** (ID: {animal_id}) set to **{nickname}**!"
    )
    
# Slash command with optional page parameter
@bot.tree.command(name="animalslist", description="View your captured animals list (10 per page)")
@app_commands.describe(page="Optional: page number to jump to")
async def animalslist(interaction: discord.Interaction, page: int = 1):
    table_name = str(interaction.user.id)

    async with aiosqlite.connect("owned.db") as db:
        cursor = await db.execute(f"SELECT name, nickname FROM [{table_name}]")
        rows = await cursor.fetchall()

    if not rows:
        await interaction.response.send_message("❌ You don’t own any animals yet!", ephemeral=True)
        return

    animals = [{"name": row[0], "nickname": row[1]} for row in rows]

    total_pages = (len(animals) - 1) // 10 + 1
    page = max(1, min(page, total_pages))  # clamp page number
    view = AnimalsListView(animals, interaction.user.id, page=page-1)
    await interaction.response.send_message(embed=view.get_embed(), view=view)
    
@bot.tree.command(name="choosecompanion", description="Choose one of your owned animals as your companion")
@app_commands.describe(animal_id="The ID of the animal you want to use as your companion")
async def choosecompanion(interaction: discord.Interaction, animal_id: int):
    user_id = interaction.user.id

    # Step 1: Check if this animal exists in owned.db
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

        cursor = await db.execute(f"SELECT id, name, nickname FROM [{user_id}] WHERE id = ?", (animal_id,))
        animal = await cursor.fetchone()

    if not animal:
        await interaction.response.send_message("❌ You don’t own an animal with that ID.", ephemeral=True)
        return

    # Step 2: Update playerdata.db with companion id
    async with aiosqlite.connect("playerdata.db") as db:
        await db.execute(f""" 
            CREATE TABLE IF NOT EXISTS [{user_id}] (
                balance INTEGER,
                health INTEGER,
                deathcount INTEGER,
                location TEXT,
                inventory TEXT,
                creationdate TEXT,
                winstreak INTEGER,
                highstreak INTEGER,
                companion INTEGER
            )
        """)
        await db.execute(f"UPDATE [{user_id}] SET companion = ?", (animal_id,))
        await db.commit()

    # Step 3: Confirmation
    name_display = animal[2] if animal[2] else animal[1]  # nickname if exists, else name
    await interaction.response.send_message(f"✅ You chose **{name_display}** (ID: {animal_id}) as your companion!")
                    
keep_alive()
bot.run(token)  