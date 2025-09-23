import discord
import math

class Location:
    def __init__(self, biome, terrain , time, disaster, loot,image):
        self.biome = biome
        self.terrain = terrain
        self.time = time
        self.disaster = disaster
        self.loot = loot
        self.image = image
        
class Animal:
    def __init__(self, name, scientific_name, nature,habitat,ability, health, attack, defense, speed, catagory, rarity, drops,sprite,description,moves,healthp=0,attackp=0,defensep=0,speedp=0,training=0):
        self.name = name
        self.scientific_name = scientific_name
        self.nature = nature
        self.habitat = habitat
        self.ability = ability
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.catagory = catagory
        self.rarity = rarity
        self.drops = drops
        self.sprite = sprite
        self.description = description
        self.moves = moves
        self.healthp = healthp
        self.attackp = attackp
        self.defensep = defensep
        self.speedp = speedp
        self.training = training
        
class BattleAnimal:
    def __init__(self, name, sprite,catagory, ability, nature, moves, drop, health,attack,defense,speed):
        self.name = name
        self.sprite = sprite
        self.catagory = catagory
        self.ability = ability
        self.moves = moves
        self.nature = nature
        self.status = "Alive"
        self.drop = drop
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.flinch = False
        self.confused = False
        self.attackboost = 0
        self.defenseboost = 0
        self.speedboost = 0
        self.maxhealth = health
        
class Player:
    def __init__(self, name, location, inventory,idt):
        self.name = name
        self.location = location
        self.inventory = inventory
        self.id = idt

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