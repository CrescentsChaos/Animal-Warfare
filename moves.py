import random

async def finslash(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 60
    movetype="Aquatic"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def predatorysurge(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 90
    movetype="Aquatic"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def venomousfang(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 60
    movetype="Venomous"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
    await poison(attacker,defender,50,embed)
    
async def piercingbeak(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 70
    movetype="Flying"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost,crit=30)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def suction(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 30
    movetype="Aquatic"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def gore(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 80
    movetype="Giant"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def electricution(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 50
    movetype="Aquatic"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
    await paralyze(attacker,defender,50,embed)
    
async def deathroll(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 80
    movetype="Aquatic"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
    await bleed(attacker,defender,70,embed)
    
async def tackle(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 40
    movetype="Giant"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def scratch(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 50
    movetype="Agile"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def bite(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 65
    movetype="Predator"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def peck(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 30
    movetype="Flying"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
    
async def pounce(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 50
    movetype="Agile"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
        
async def tailwhip(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 20
    movetype="Armored"
    catboost=await get_damage_multiplier(attacker, defender,movetype)
    damage= await dmg(attacker, defender, base_damage, move, field,embed,catboost)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
    await defensechange(defender,attacker,50,-0.25,embed,defender)
    
async def howl(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 20
    movetype="Predator"
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"Howl was heard from miles away!", inline=False)
    await attackchange(attacker,attacker,100,0.5,embed,defender)
    
#Damage Calculation        
async def dmg(attacker, defender, base_damage, move, field,embed,catboost=1,crit=5):
    critchance=random.randint(1,100)
    critdmg=1
    if critchance<=crit:
        critdmg=1.5
        embed.add_field(name="Critcial hit!",value=f"{attacker.name} landed a critical hit.",inline=False)
    # Simple damage formula considering attack and defense stats
    damage = (base_damage * (attacker.attack*attacker.attackboost / defender.defense*defender.defenseboost)*random.randint(85, 100) / 100)*catboost*critdmg*(attacker.maxhealth/defender.maxhealth)
    return max(1, round(damage))  # Ensure at least 1 damage is done  

async def get_damage_multiplier(ally, foe, movetype: str) -> float:
    """
    Returns the damage multiplier based on ally and foe categories.
    movetype is one of: Predator, Prey, Scavenger, Parasite, Armored,
    Agile, Tiny, Giant, Social, Solitary, Flying, Aquatic, Burrowing,
    Arboreal, Poisonous, Venomous.
    """

    TYPE_CHART = {
        "Predator": {
            "Prey": 2.0, "Scavenger": 1.5, "Predator": 1.0,
            "Armored": 0.5, "Agile": 1.2, "Tiny": 1.0, "Giant": 0.8,
            "Solitary": 1.0, "Social": 0.8, "Flying": 0.9, "Aquatic": 1.0,
            "Burrowing": 0.7, "Arboreal": 0.8, "Poisonous": 0.5, "Venomous": 0.5
        },
        "Prey": {
            "Predator": 0.5, "Prey": 1.0, "Scavenger": 0.5,
            "Armored": 0.5, "Agile": 1.2, "Tiny": 1.0, "Giant": 0.8,
            "Solitary": 1.0, "Social": 1.1, "Flying": 1.1, "Aquatic": 1.0,
            "Burrowing": 1.1, "Arboreal": 1.0, "Poisonous": 0.8, "Venomous": 0.8
        },
        "Scavenger": {
            "Predator": 0.5, "Prey": 1.5, "Scavenger": 1.0,
            "Armored": 0.7, "Agile": 1.0, "Tiny": 1.0, "Giant": 0.5,
            "Solitary": 1.0, "Social": 1.2, "Flying": 1.0, "Aquatic": 1.0,
            "Burrowing": 1.0, "Arboreal": 0.8, "Poisonous": 0.5, "Venomous": 0.5
        },
        "Parasite": {
            "Giant": 1.5, "Tiny": 2.0, "Solitary": 1.2, "Social": 1.5,
            "Predator": 0.7, "Prey": 1.0, "Armored": 0.5, "Agile": 0.8,
            "Flying": 0.8, "Aquatic": 1.0, "Burrowing": 1.0, "Arboreal": 1.0,
            "Poisonous": 0.5, "Venomous": 0.5
        },
        "Armored": {
            "Predator": 0.5, "Prey": 1.0, "Scavenger": 1.0,
            "Agile": 0.8, "Tiny": 1.0, "Giant": 1.2, "Solitary": 1.0,
            "Social": 1.0, "Flying": 0.7, "Aquatic": 0.9, "Burrowing": 1.0,
            "Arboreal": 0.8, "Poisonous": 1.0, "Venomous": 1.0
        },
        "Agile": {
            "Predator": 1.2, "Prey": 1.0, "Scavenger": 1.0,
            "Armored": 0.7, "Tiny": 1.0, "Giant": 0.8, "Solitary": 1.0,
            "Social": 0.9, "Flying": 1.0, "Aquatic": 1.0, "Burrowing": 1.1,
            "Arboreal": 1.1, "Poisonous": 0.9, "Venomous": 0.9
        },
        "Tiny": {
            "Predator": 0.5, "Prey": 1.0, "Scavenger": 1.0,
            "Armored": 0.3, "Agile": 1.0, "Giant": 0.5, "Solitary": 1.0,
            "Social": 1.1, "Flying": 1.0, "Aquatic": 1.0, "Burrowing": 1.2,
            "Arboreal": 1.0, "Poisonous": 1.5, "Venomous": 1.5
        },
        "Giant": {
            "Predator": 1.0, "Prey": 2.0, "Scavenger": 1.0,
            "Armored": 1.2, "Agile": 0.8, "Tiny": 1.0, "Solitary": 1.0,
            "Social": 0.9, "Flying": 0.5, "Aquatic": 1.0, "Burrowing": 0.7,
            "Arboreal": 0.5, "Poisonous": 0.7, "Venomous": 0.7
        },
        "Social": {
            "Predator": 0.8, "Prey": 1.2, "Scavenger": 1.0,
            "Armored": 1.0, "Agile": 1.0, "Tiny": 1.1, "Giant": 0.9,
            "Solitary": 0.8, "Flying": 1.0, "Aquatic": 1.0, "Burrowing": 1.0,
            "Arboreal": 1.0, "Poisonous": 0.9, "Venomous": 0.9
        },
        "Solitary": {
            "Predator": 1.0, "Prey": 1.0, "Scavenger": 1.0,
            "Armored": 1.0, "Agile": 1.0, "Tiny": 1.0, "Giant": 1.0,
            "Social": 1.2, "Flying": 1.0, "Aquatic": 1.0, "Burrowing": 1.0,
            "Arboreal": 1.0, "Poisonous": 1.0, "Venomous": 1.0
        },
        "Flying": {
            "Predator": 1.0, "Prey": 1.1, "Scavenger": 1.0,
            "Armored": 0.8, "Agile": 1.2, "Tiny": 1.0, "Giant": 0.5,
            "Solitary": 1.0, "Social": 1.0, "Aquatic": 0.9, "Burrowing": 1.1,
            "Arboreal": 1.0, "Poisonous": 0.9, "Venomous": 0.9
        },
        "Aquatic": {
            "Predator": 1.0, "Prey": 1.0, "Scavenger": 1.0,
            "Armored": 1.0, "Agile": 1.0, "Tiny": 1.0, "Giant": 1.0,
            "Solitary": 1.0, "Social": 1.0, "Flying": 0.9, "Burrowing": 1.0,
            "Arboreal": 0.8, "Poisonous": 0.9, "Venomous": 0.9
        },
        "Burrowing": {
            "Predator": 0.7, "Prey": 1.1, "Scavenger": 1.0,
            "Armored": 1.0, "Agile": 1.0, "Tiny": 1.1, "Giant": 0.7,
            "Solitary": 1.0, "Social": 1.0, "Flying": 0.8, "Aquatic": 1.0,
            "Arboreal": 0.7, "Poisonous": 1.0, "Venomous": 1.0
        },
        "Arboreal": {
            "Predator": 0.8, "Prey": 1.0, "Scavenger": 0.8,
            "Armored": 0.8, "Agile": 1.2, "Tiny": 1.0, "Giant": 0.5,
            "Solitary": 1.0, "Social": 1.0, "Flying": 1.0, "Aquatic": 0.7,
            "Burrowing": 0.7, "Poisonous": 0.9, "Venomous": 0.9
        },
        "Poisonous": {
            "Predator": 1.5, "Prey": 0.8, "Scavenger": 1.2,
            "Armored": 0.9, "Agile": 1.0, "Tiny": 1.5, "Giant": 1.0,
            "Solitary": 1.0, "Social": 0.9, "Flying": 1.0, "Aquatic": 1.0,
            "Burrowing": 1.0, "Arboreal": 1.0, "Venomous": 1.2
        },
        "Venomous": {
            "Predator": 1.5, "Prey": 0.8, "Scavenger": 1.2,
            "Armored": 0.9, "Agile": 1.0, "Tiny": 1.5, "Giant": 1.0,
            "Solitary": 1.0, "Social": 0.9, "Flying": 1.0, "Aquatic": 1.0,
            "Burrowing": 1.0, "Arboreal": 1.0, "Poisonous": 1.2
        },
    }

    # Default multiplier
    multiplier = 1.0

    # Ensure categories are lists
    ally_types = ally.category.split(",") if isinstance(ally.category, str) else ally.category
    foe_types = foe.category.split(",") if isinstance(foe.category, str) else foe.category

    # Compute multiplier based on movetype vs foe categories
    for ftype in foe_types:
        multiplier *= TYPE_CHART.get(movetype, {}).get(ftype, 1.0)
    if movetype in ally_types:
        multiplier*=1.1
    print(ally.name,round(multiplier,2))
    return round(multiplier,2)

async def paralyze(attacker,defender,percentage,embed):
    chance=random.randint(1,100)
    if chance<=percentage and "Paralyzed" not in defender.status:
        defender.status.append("Paralyzed")
        embed.add_field(name="Paralyzed!",value=f"{defender.name} is paralyzed.",inline=False)
        
async def bleed(attacker,defender,percentage,embed):
    chance=random.randint(1,100)
    if chance<=percentage and "Bleed" not in defender.status:
        defender.status.append("Bleed")
        embed.add_field(name="Bleed!",value=f"{defender.name} is bleeding.",inline=False)

async def poison(attacker,defender,percentage,embed):
    chance=random.randint(1,100)
    if chance<=percentage and "Poison" not in defender.status:
        defender.status.append("Poison")
        embed.add_field(name="Poisoned!",value=f"{defender.name} was poisoned.",inline=False)

async def sleep(attacker,defender,percentage,embed):
    chance=random.randint(1,100)
    if chance<=percentage and "Sleep" not in defender.status:
        defender.status.append("Sleep")
        embed.add_field(name="Sleep!",value=f"{defender.name} fell asleep.",inline=False)

async def drown(attacker,defender,percentage,embed):
    chance=random.randint(1,100)
    if chance<=percentage and "Drown" not in defender.status:
        defender.status.append("Drown")
        embed.add_field(name="Drown!",value=f"{defender.name} is drowning.",inline=False)
                        
async def attackchange(victim,attacker,percentage,boost,embed,defender):
    chance=random.randint(1,100)
    if chance<=percentage and victim.attackboost!=3 and boost>0:
        if boost==0.5:
            victim.attackboost+=0.5
            embed.add_field(name="Attack boosted!",value=f"{victim.name}'s attack rose.",inline=False)
        elif boost==1:
            victim.attackboost+=1
            embed.add_field(name="Attack boosted!",value=f"{victim.name}'s attack sharply rose.",inline=False)
        if victim.attackboost>3:
            victim.attackboost=3
    elif chance<=percentage and victim.attackboost==3 and boost>0:
        embed.add_field(name="Attack boost attempt!",value=f"{victim.name}'s attack won't go any higher.",inline=False)
    elif chance<=percentage and victim.attackboost!=3 and boost<0:
        if boost==-0.25:
            victim.attackboost-=0.5
            embed.add_field(name="Attack nerfed!",value=f"{victim.name}'s attack fell.",inline=False)
        elif boost==-1:
            victim.attackboost-=0.5
            embed.add_field(name="Attack nerfed!",value=f"{victim.name}'s attack heavily fell.",inline=False)
        if victim.attackboost<0.25:
            victim.attackboost=0.25
    elif chance<=percentage and victim.attackboost==0.25 and boost<0:
        embed.add_field(name="Attack nerf attempt!",value=f"{victim.name}'s attack won't go any lower.",inline=False)

async def defensechange(victim,attacker,percentage,boost,embed,defender):
    chance=random.randint(1,100)
    if chance<=percentage and victim.defenseboost!=3 and boost>0:
        if boost==0.5:
            victim.defenseboost+=0.5
            embed.add_field(name="Defense boosted!",value=f"{victim.name}'s defense rose.",inline=False)
        elif boost==1:
            victim.defenseboost+=1
            embed.add_field(name="Defense boosted!",value=f"{victim.name}'s defense sharply rose.",inline=False)
        if victim.defenseboost>3:
            victim.defenseboost=3
    elif chance<=percentage and victim.defenseboost==3 and boost>0:
        embed.add_field(name="Defense boost attempt!",value=f"{victim.name}'s defense won't go any higher.",inline=False)
    elif chance<=percentage and victim.defenseboost!=3 and boost<0:
        if boost==-0.25:
            victim.defenseboost-=0.5
            embed.add_field(name="Defense nerfed!",value=f"{victim.name}'s defense fell.",inline=False)
        elif boost==-1:
            victim.defenseboost-=0.5
            embed.add_field(name="Defense nerfed!",value=f"{victim.name}'s defensek heavily fell.",inline=False)
        if victim.defenseboost<0.25:
            victim.defenseboost=0.25
    elif chance<=percentage and victim.defenseboost==0.25 and boost<0:
        embed.add_field(name="Defense nerf attempt!",value=f"{victim.name}'s defense won't go any lower.",inline=False)
    