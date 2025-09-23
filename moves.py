import random

async def tackle(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 40
    damage= await dmg(attacker, defender, base_damage, move, field,embed)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def scratch(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 50
    damage= await dmg(attacker, defender, base_damage, move, field,embed)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def bite(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 60
    damage= await dmg(attacker, defender, base_damage, move, field,embed)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)

async def peck(attacker,defender,move,player,foe,field,embed):
    # Basic damage calculation
    base_damage = 30
    damage= await dmg(attacker, defender, base_damage, move, field,embed)
    defender.health -= damage
    embed.add_field(name=f"{attacker.name} used {move}!", value=f"It dealt {damage} damage!", inline=False)
    
    
async def dmg(attacker, defender, base_damage, move, field,embed):
    # Simple damage formula considering attack and defense stats
    damage = base_damage * (attacker.attack / defender.defense)*random.randint(85, 100) / 100

    return max(1, int(damage))  # Ensure at least 1 damage is done  