class Location:
    def __init__(self, biome, terrain , time, disaster, loot,image):
        self.biome = biome
        self.terrain = terrain
        self.time = time
        self.disaster = disaster
        self.loot = loot
        self.image = image
        
class Animal:
    def __init__(self, name, scientific_name, habitat,ability, health, attack, defense, speed, catagory, rarity, drops,sprite,description,moves):
        self.name = name
        self.scientific_name = scientific_name
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
class Player:
    def __init__(self, name, location, inventory):
        self.name = name
        self.location = location
        self.inventory = inventory