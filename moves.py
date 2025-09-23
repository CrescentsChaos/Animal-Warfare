import random

async def tackle(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 40
    catboost=await get_damage_multiplier(attacker, defender)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def scratch(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 50
    catboost=await get_damage_multiplier(attacker, defender)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def bite(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 65
    catboost=await get_damage_multiplier(attacker, defender)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def peck(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 30
    catboost=await get_damage_multiplier(attacker, defender)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
    
async def pounce(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 50
    catboost=await get_damage_multiplier(attacker, defender)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
        
async def tailwhip(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 20
    catboost=await get_damage_multiplier(attacker, defender)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
        
async def dmg(attacker, defender, base_damage, move, field,embed,catboost=1):
    # Simple damage formula considering attack and defense stats
    damage = (base_damage * (attacker.attack / defender.defense)*random.randint(85, 100) / 100)*catboost

    return max(1, int(damage))  # Ensure at least 1 damage is done  

async def get_damage_multiplier(ally, foe):
    TYPE_CHART = {
    "Predator": {"Predator": 1.0, "Scavenger": 2.0, "Aquatic": 1.0, "Prey":2.0,"Domestic":2.0},
    "Scavenger": {"Predator": 0.5, "Scavenger": 1.0, "Aquatic": 1.0, "Prey":0.5,"Domestic":1.0},
    "Aquatic": {"Predator": 1.0, "Scavenger": 1.0, "Aquatic": 1.0, "Prey":1.0,"Domestic":1.0},
    "Prey":{"Predator": 0.5, "Scavenger": 0.5, "Aquatic": 1.0, "Prey":1.0,"Domestic":1.0},
    "Domestic":{"Predator": 1.0, "Scavenger": 1.0, "Aquatic": 1.0, "Prey":1.0,"Domestic":1.0},
    # Add more categories as needed
}
    """
    Returns the damage multiplier based on ally and foe categories.
    """
    ally_type = ally.category.split(",")
    foe_type = foe.category.split(",")

    # Default multiplier if types not defined
    multiplier = 1.0

    for ally_type in ally.category:  # ally.category is a list
        for foe_type in foe.category:  # foe.category is a list
            if ally_type in TYPE_CHART:
                multiplier *= TYPE_CHART[ally_type].get(foe_type, 1.0)

    return multiplier 