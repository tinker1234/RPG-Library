# RPG Library

A comprehensive Python library for creating RPG (Role-Playing Game) systems with leveling, abilities, shops, enemies, and item management.

## Features

- **Player System**: Character creation with leveling, experience, and stat allocation
- **Enemy System**: Customizable enemies with AI, abilities, and drop tables
- **Ability System**: Combat abilities with cooldowns, mana costs, and various effects
- **Item System**: Weapons, armor, consumables with equipment and stat bonuses
- **Shop System**: Easy-to-create shops with buying/selling mechanics
- **Factory Classes**: Convenient creation of common items, abilities, and enemies

## Quick Start

```python
from rpg_core import Player, Shop
from rpg_factory import ItemFactory, AbilityFactory, EnemyFactory, ShopFactory

# Create a player
player = Player("Hero", hp=100, mana=50, attack=10, defense=5)

# Add abilities
player.add_ability(AbilityFactory.slash())
player.add_ability(AbilityFactory.heal())

# Create an enemy
goblin = EnemyFactory.goblin(level=2)

# Create a shop
shop = ShopFactory.create_weapon_shop()
```

## Core Classes

### Character (Base Class)

The base class for all characters (Player and Enemy) with core functionality:

```python
from rpg_core import Character, StatusEffectType

# Character provides the foundation for all game entities
character = Character("Base Character", hp=100, mana=50, attack=10, defense=5)

# Core methods available to all characters
character.add_ability(ability)           # Add an ability
character.add_item(item)                 # Add item to inventory
character.equip_item(item, "weapon")     # Equip items in slots
character.unequip_item("weapon")         # Remove equipped items
character.use_item(item)                 # Use consumable items

# Status effect management
character.add_status_effect(status_effect)              # Apply status effect
character.remove_status_effect(StatusEffectType.POISON) # Remove specific effect
character.has_status_effect(StatusEffectType.BURN)      # Check for effect
character.process_status_effects()                      # Process all effects per turn
character.is_action_prevented()                         # Check if stunned/frozen

# Combat and stat calculations
total_attack = character.get_total_attack()    # Attack + equipment + status effects
total_defense = character.get_total_defense()  # Defense + equipment + status effects
character.take_damage(amount)                  # Apply damage with defense calculation
character.heal(amount)                         # Restore HP (capped at max_hp)
character.restore_mana(amount)                 # Restore mana (capped at max_mana)

# Ability management
character.update_cooldowns()                   # Reduce all ability cooldowns by 1

# Status checks
character.is_alive()                           # Check if HP > 0
```

### StatusEffect

Represents temporary effects that modify character behavior:

```python
from rpg_core import StatusEffect, StatusEffectType

# Create custom status effects
poison = StatusEffect(
    name="Deadly Poison",
    effect_type=StatusEffectType.POISON,
    duration=5,           # Lasts 5 turns
    power=8,             # Deals 8 damage per turn
    description="A lethal toxin"
)

# Status effect types and their behaviors:
# POISON, BURN - Deal damage each turn (power = damage per turn)
# FREEZE, STUN - Prevent actions (power ignored)
# STRENGTH_BOOST, WEAKNESS - Modify attack (power = attack modifier)
# DEFENSE_BOOST, VULNERABILITY - Modify defense (power = defense modifier)
# REGENERATION - Heal each turn (power = healing per turn)

# Status effects automatically process each turn
messages = character.process_status_effects()  # Returns list of effect messages
```

### Player

The main character class with leveling and progression.

```python
player = Player("Hero", hp=100, mana=50, attack=10, defense=5)

# Leveling system
level_up_msg = player.gain_experience(100)  # Returns message if leveled up
player.allocate_stat_point("attack")        # Spend stat points from leveling
player.allocate_stat_point("defense")       # Available stats: attack, defense, hp, mana
player.allocate_stat_point("hp")
player.allocate_stat_point("mana")

# Player-specific attributes
print(f"Level: {player.level}")
print(f"Experience: {player.experience}/{player.experience_to_next_level}")
print(f"Gold: {player.gold}")
print(f"Stat Points: {player.stat_points}")

# Equipment system
sword = ItemFactory.create_weapon("Steel Sword", 10, 50)
player.add_item(sword)
player.equip_item(sword, "weapon")

# Abilities
fireball = AbilityFactory.fireball()
player.add_ability(fireball)
result = fireball.use(player, target)  # Returns result message
```

### Enemy

Customizable enemies with AI and drop systems.

```python
# Using factory for common enemies
orc = EnemyFactory.orc(level=3)

# Creating custom enemies
custom_enemy = EnemyFactory.create_custom_enemy(
    name="Shadow Beast",
    hp=80, mana=40, attack=15, defense=8,
    level=5,
    abilities=[AbilityFactory.slash(), AbilityFactory.heal()],
    drops=[(ItemFactory.create_weapon("Dark Blade", 12, 100), 0.3)]
)

# Enemy-specific attributes
print(f"Level: {enemy.level}")
print(f"EXP Reward: {enemy.exp_reward}")
print(f"Gold Reward: {enemy.gold_reward}")

# Drop system management
enemy.add_drop(item, 0.3)           # Add item with 30% drop chance
drops = enemy.get_drops()           # Get random drops based on probabilities

# AI system
chosen_ability = enemy.ai_choose_ability(player)  # AI selects best ability
if chosen_ability:
    result = chosen_ability.use(enemy, player)
```

### Item

Represents all items in the game with type-based functionality:

```python
from rpg_core import Item, ItemType

# Create items manually
weapon = Item(
    name="Excalibur",
    item_type=ItemType.WEAPON,
    value=500,
    description="A legendary sword",
    stats={"attack": 25}  # Stat bonuses when equipped
)

# Item types and their purposes:
# WEAPON - Provides attack bonus when equipped
# ARMOR - Provides defense bonus when equipped  
# CONSUMABLE - Can be used for immediate effects
# MISC - General items with no special mechanics

# Item attributes
print(f"Name: {item.name}")
print(f"Type: {item.item_type}")
print(f"Value: {item.value} gold")
print(f"Stats: {item.stats}")
print(f"Description: {item.description}")
```

### Ability

Represents skills, spells, and attacks that characters can use:

```python
from rpg_core import Ability, AbilityType, StatusEffect, StatusEffectType

# Create abilities manually
fireball = Ability(
    name="Fireball",
    ability_type=AbilityType.ATTACK,
    power=25,                    # Damage or healing amount
    mana_cost=10,               # Mana required to use
    description="A magical fireball",
    cooldown=2,                 # Turns before reuse
    status_effect=burn_effect   # Optional status effect to apply
)

# Ability types:
# ATTACK - Deals damage to target
# HEAL - Restores HP to target
# BUFF - Applies beneficial status effect
# DEBUFF - Applies harmful status effect

# Ability usage and management
can_use = ability.can_use(caster)           # Check mana and cooldown
result = ability.use(caster, target)        # Use ability and get result message
ability.reduce_cooldown()                   # Reduce cooldown by 1

# Ability attributes
print(f"Current Cooldown: {ability.current_cooldown}")
print(f"Max Cooldown: {ability.cooldown}")
print(f"Mana Cost: {ability.mana_cost}")
print(f"Power: {ability.power}")
```

### Shop

Easy shop creation and management.

```python
# Pre-made shops
weapon_shop = ShopFactory.create_weapon_shop()
armor_shop = ShopFactory.create_armor_shop()
potion_shop = ShopFactory.create_potion_shop()
general_shop = ShopFactory.create_general_shop()

# Custom shops
custom_shop = Shop("Magic Items")
custom_shop.add_item(ItemFactory.create_weapon("Magic Sword", 20, 200))

# Shop management
shop.add_item(item, quantity=3)         # Add multiple copies of an item
shop.remove_item(item_name)             # Remove item from inventory
items = shop.list_items()               # Get all available items

# Pricing (direct attribute access)
shop.buy_price_multiplier = 1.2     # Adjust buying prices (default 1.0)
shop.sell_price_multiplier = 0.4    # Adjust selling prices (default 0.5)

# Transactions
success = shop.buy_item(player, magic_sword)  # Player buys from shop
success = shop.sell_item(player, old_sword)   # Shop buys from player

# Shop attributes
print(f"Shop Name: {shop.name}")
print(f"Items in stock: {len(shop.inventory)}")
print(f"Buy multiplier: {shop.buy_price_multiplier}")
print(f"Sell multiplier: {shop.sell_price_multiplier}")
```

## Factory Classes

### ItemFactory

Create various types of items easily:

```python
# Weapons with attack bonuses
sword = ItemFactory.create_weapon("Steel Sword", attack_bonus=10, price=50)
bow = ItemFactory.create_weapon("Longbow", attack_bonus=8, price=40, description="Ranged weapon")

# Armor with defense bonuses
armor = ItemFactory.create_armor("Chain Mail", defense_bonus=5, price=60)
shield = ItemFactory.create_armor("Iron Shield", defense_bonus=3, price=30)

# Consumables for immediate use
health_potion = ItemFactory.create_health_potion(healing_amount=50)
mana_potion = ItemFactory.create_mana_potion(mana_amount=30)
custom_potion = ItemFactory.create_consumable("Super Potion", price=100, description="Heals everything")

# All ItemFactory methods:
ItemFactory.create_weapon(name, attack_bonus, value=None, description="")
ItemFactory.create_armor(name, defense_bonus, value=None, description="")
ItemFactory.create_consumable(name, value, description="")
ItemFactory.create_health_potion(healing_power=50)  # Restores HP
ItemFactory.create_mana_potion(mana_power=30)       # Restores mana
```

### AbilityFactory

Create abilities with different effects:

```python
# Basic attack abilities
slash = AbilityFactory.slash()              # Basic physical attack (15 damage, no cost)
power_strike = AbilityFactory.power_strike() # Strong attack (35 damage, 5 mana, 2 cooldown)
fireball = AbilityFactory.fireball()        # Magic attack (25 damage, 10 mana, 1 cooldown)

# Healing abilities
heal = AbilityFactory.heal()                # Basic healing (30 HP, 8 mana)

# Status effect abilities - Damage over time
poison_dart = AbilityFactory.poison_dart()      # Poison effect (3 turns, 5 damage/turn)
flame_strike = AbilityFactory.flame_strike()    # Burn effect (3 turns, 8 damage/turn)

# Status effect abilities - Crowd control
ice_shard = AbilityFactory.ice_shard()          # Freeze effect (2 turns)
stunning_blow = AbilityFactory.stunning_blow()  # Stun effect (1 turn)

# Status effect abilities - Debuffs
weakness_curse = AbilityFactory.weakness_curse() # Reduces attack (-8 for 4 turns)
armor_break = AbilityFactory.armor_break()       # Reduces defense (-6 for 3 turns)

# Status effect abilities - Buffs
battle_cry = AbilityFactory.battle_cry()        # Increases attack (+10 for 5 turns)
shield_wall = AbilityFactory.shield_wall()      # Increases defense (+8 for 4 turns)

# Custom abilities
custom_ability = AbilityFactory.create_attack_ability(
    name="Lightning Bolt",
    power=25,
    mana_cost=15,
    cooldown=3,
    description="Strikes with lightning"
)

custom_heal = AbilityFactory.create_heal_ability(
    name="Greater Heal",
    power=50,
    mana_cost=15,
    cooldown=2,
    description="Powerful healing spell"
)

custom_buff = AbilityFactory.create_buff_ability(
    name="Divine Blessing",
    mana_cost=20,
    cooldown=5,
    description="Grants divine protection"
)

# Status effect abilities
status_ability = AbilityFactory.create_status_effect_ability(
    name="Toxic Cloud",
    power=10,                           # Base damage
    mana_cost=12,
    status_effect_type=StatusEffectType.POISON,
    effect_duration=5,                  # Lasts 5 turns
    effect_power=6,                     # 6 poison damage per turn
    cooldown=3,
    description="Creates a poisonous cloud"
)
```

### EnemyFactory

Create enemies with predefined stats and abilities:

```python
# Common enemies (level scales stats automatically)
goblin = EnemyFactory.goblin(level=1)           # Weak melee enemy
orc = EnemyFactory.orc(level=3)                 # Strong melee enemy
skeleton_mage = EnemyFactory.skeleton_mage(level=4)  # Magic user
dragon = EnemyFactory.dragon(level=10)          # Boss enemy

# Specialized enemies
spider = EnemyFactory.venomous_spider(level=2)  # Poison attacks
frost_elem = EnemyFactory.frost_elemental(level=5)  # Ice abilities
fire_demon = EnemyFactory.fire_demon(level=6)  # Fire abilities
assassin = EnemyFactory.shadow_assassin(level=7)  # High damage, low HP
shaman = EnemyFactory.nature_shaman(level=4)   # Healing and buffs

# Custom enemy with specific configuration
boss = EnemyFactory.create_custom_enemy(
    name="Dark Lord",
    hp=200, mana=100, attack=25, defense=15,
    level=15,
    exp_reward=500,     # Optional: defaults to level * 20 + random
    gold_reward=250,    # Optional: defaults to level * 8 + random
    abilities=[
        AbilityFactory.fireball(),
        AbilityFactory.power_strike(),
        AbilityFactory.heal()
    ],
    drops=[
        (ItemFactory.create_weapon("Dark Sword", 30, 500), 1.0),  # 100% drop
        (ItemFactory.create_armor("Dark Armor", 20, 400), 0.5),   # 50% drop
    ]
)
```

### ShopFactory

Create pre-stocked shops with themed inventories:

```python
# Pre-made themed shops
weapon_shop = ShopFactory.create_weapon_shop()    # Various weapons
armor_shop = ShopFactory.create_armor_shop()      # Armor and shields
potion_shop = ShopFactory.create_potion_shop()    # Health and mana potions
general_shop = ShopFactory.create_general_shop()  # Mixed inventory

# Each shop comes pre-stocked with appropriate items
# Weapon shop: Iron Sword, Steel Sword, Silver Dagger, War Hammer, Magic Staff
# Armor shop: Leather Armor, Chain Mail, Plate Armor, Iron Shield, Steel Shield
# Potion shop: Health Potions, Mana Potions, various healing items
# General shop: Mix of weapons, armor, and consumables
```

## Status Effects System

The library includes a comprehensive status effects system that adds depth to combat:

### Available Status Effects

- **Damage Over Time**: `POISON`, `BURN` - Deal damage each turn
- **Crowd Control**: `FREEZE`, `STUN` - Prevent actions for duration
- **Stat Modifiers**: `STRENGTH_BOOST`, `WEAKNESS` - Modify attack power
- **Defense Modifiers**: `DEFENSE_BOOST`, `VULNERABILITY` - Modify defense
- **Healing Over Time**: `REGENERATION` - Restore HP each turn

### Using Status Effects

```python
# Create abilities that apply status effects
poison_dart = AbilityFactory.poison_dart()  # Applies poison
flame_strike = AbilityFactory.flame_strike()  # Applies burn
ice_shard = AbilityFactory.ice_shard()  # Can freeze target
battle_cry = AbilityFactory.battle_cry()  # Self-buff for attack

# Status effects are automatically applied when abilities are used
result = poison_dart.use(player, enemy)  # Enemy gets poisoned

# Check for status effects
if enemy.has_status_effect(StatusEffectType.POISON):
    print("Enemy is poisoned!")

# Process status effects each turn
messages = character.process_status_effects()
for message in messages:
    print(message)  # Shows damage, healing, or effect expiration

# Status effects modify stats automatically
total_attack = character.get_total_attack()  # Includes status effect bonuses/penalties
total_defense = character.get_total_defense()  # Includes status effect bonuses/penalties
```

### Creating Custom Status Effect Abilities

You can create abilities that apply status effects upon use in several ways:

#### Using AbilityFactory.create_status_effect_ability()

The easiest way to create abilities with status effects is using the factory method:

```python
from rpg_core import StatusEffectType, AbilityType
from rpg_factory import AbilityFactory

# Create a custom poison ability
custom_poison = AbilityFactory.create_status_effect_ability(
    name="Deadly Venom",
    power=15,  # Base damage of the ability
    mana_cost=12,
    status_effect_type=StatusEffectType.POISON,
    effect_duration=4,  # Lasts 4 turns
    effect_power=8,  # Deals 8 poison damage per turn
    cooldown=2,
    description="A potent poison that deals damage over time"
)

# Create a buff ability
strength_buff = AbilityFactory.create_status_effect_ability(
    name="Berserker Rage",
    power=0,  # No immediate damage
    mana_cost=15,
    status_effect_type=StatusEffectType.STRENGTH_BOOST,
    effect_duration=5,
    effect_power=10,  # +10 attack for 5 turns
    cooldown=8,
    description="Increases attack power temporarily"
)
strength_buff.ability_type = AbilityType.BUFF  # Make it a buff ability
```

#### Manual Ability Creation with Status Effects

You can also create abilities manually by setting the status_effect parameter:

```python
from rpg_core import Ability, StatusEffect, StatusEffectType, AbilityType

# Create the status effect first
burn_effect = StatusEffect(
    name="Burning Flames",
    effect_type=StatusEffectType.BURN,
    duration=3,
    power=6,  # Damage per turn
    description="Burns the target with magical flames"
)

# Create the ability with the status effect
fire_spell = Ability(
    name="Flame Bolt",
    ability_type=AbilityType.ATTACK,
    power=20,  # Initial damage
    mana_cost=10,
    description="A bolt of fire that burns the target",
    cooldown=1,
    status_effect=burn_effect  # Attach the status effect
)

# The ability will now apply the burn effect when used
```

#### Pre-made Status Effect Abilities

The AbilityFactory provides many pre-made abilities with status effects:

```python
# Damage over time abilities
poison_dart = AbilityFactory.poison_dart()      # Poison effect
flame_strike = AbilityFactory.flame_strike()    # Burn effect

# Crowd control abilities
ice_shard = AbilityFactory.ice_shard()          # Freeze effect
stunning_blow = AbilityFactory.stunning_blow()  # Stun effect

# Debuff abilities
weakness_curse = AbilityFactory.weakness_curse()  # Reduces attack
armor_break = AbilityFactory.armor_break()       # Reduces defense

# Buff abilities
battle_cry = AbilityFactory.battle_cry()        # Increases attack
shield_wall = AbilityFactory.shield_wall()      # Increases defense
```

#### Status Effect Parameters Explained

When creating status effect abilities, these parameters control the effect:

- **power**: Base damage/healing of the ability itself
- **status_effect_type**: Type of status effect to apply
- **effect_duration**: How many turns the effect lasts
- **effect_power**: Strength of the status effect (damage per turn, stat bonus, etc.)
- **cooldown**: Turns before the ability can be used again

```python
# Example: Create a powerful regeneration ability
healing_aura = AbilityFactory.create_status_effect_ability(
    name="Healing Aura",
    power=25,  # Immediate healing
    mana_cost=20,
    status_effect_type=StatusEffectType.REGENERATION,
    effect_duration=6,  # Heals for 6 turns
    effect_power=12,    # Heals 12 HP per turn
    cooldown=5,
    description="Provides immediate healing and regeneration over time"
)
healing_aura.ability_type = AbilityType.HEAL  # Set as healing ability
```

## Combat System

The library includes a flexible combat system with status effect integration:

```python
# Basic combat flow with status effects
if ability.can_use(player):
    result = ability.use(player, enemy)
    print(result)

# Process status effects each turn
player_effects = player.process_status_effects()
enemy_effects = enemy.process_status_effects()

# Status effects can prevent actions
if not player.is_action_prevented():  # Check for stun/freeze
    # Player can act normally
    pass
else:
    print(f"{player.name} is unable to act due to status effects!")

# Enemy AI considers status effects when choosing abilities
enemy_ability = enemy.ai_choose_ability(player)
if enemy_ability:
    result = enemy_ability.use(enemy, player)

# Update cooldowns each turn
player.update_cooldowns()
enemy.update_cooldowns()
```

## Item Types and Equipment

Items have different types and can provide stat bonuses:

```python
# Item types
ItemType.WEAPON      # Provides attack bonus
ItemType.ARMOR       # Provides defense bonus
ItemType.CONSUMABLE  # Can be used for effects

# Equipment slots
player.equip_item(weapon, "weapon")
player.equip_item(armor, "armor")
player.equip_item(accessory, "accessory")

# Stat calculations include equipment bonuses
total_attack = player.get_total_attack()    # Base + weapon bonus
total_defense = player.get_total_defense()  # Base + armor bonus
```

## API Reference

### Enums

#### ItemType
```python
from rpg_core import ItemType

ItemType.WEAPON      # Weapons that provide attack bonuses
ItemType.ARMOR       # Armor that provides defense bonuses
ItemType.CONSUMABLE  # Items that can be used for immediate effects
ItemType.MISC        # General items with no special mechanics
```

#### AbilityType
```python
from rpg_core import AbilityType

AbilityType.ATTACK   # Abilities that deal damage
AbilityType.HEAL     # Abilities that restore HP
AbilityType.BUFF     # Abilities that apply beneficial effects
AbilityType.DEBUFF   # Abilities that apply harmful effects
```

#### StatusEffectType
```python
from rpg_core import StatusEffectType

# Damage over time effects
StatusEffectType.POISON        # Deals damage each turn
StatusEffectType.BURN          # Deals damage each turn

# Crowd control effects
StatusEffectType.FREEZE        # Prevents actions for duration
StatusEffectType.STUN          # Prevents actions for duration

# Stat modification effects
StatusEffectType.STRENGTH_BOOST    # Increases attack power
StatusEffectType.DEFENSE_BOOST     # Increases defense
StatusEffectType.SPEED_BOOST       # Increases speed (future use)
StatusEffectType.WEAKNESS          # Decreases attack power
StatusEffectType.VULNERABILITY     # Decreases defense

# Healing over time effects
StatusEffectType.REGENERATION      # Restores HP each turn
```

### Core Class Methods

#### Character Methods
```python
# Inventory and equipment
character.add_item(item: Item) -> None
character.equip_item(item: Item, slot: str = None) -> None
character.unequip_item(slot: str) -> None
character.use_item(item: Item) -> str

# Abilities
character.add_ability(ability: Ability) -> None
character.update_cooldowns() -> None

# Status effects
character.add_status_effect(status_effect: StatusEffect) -> None
character.remove_status_effect(effect_type: StatusEffectType) -> None
character.has_status_effect(effect_type: StatusEffectType) -> bool
character.process_status_effects() -> List[str]
character.is_action_prevented() -> bool

# Combat
character.take_damage(damage: int) -> str
character.heal(amount: int) -> str
character.restore_mana(amount: int) -> str
character.get_total_attack() -> int
character.get_total_defense() -> int

# Status
character.is_alive() -> bool
```

#### Player Methods
```python
# Leveling system
player.gain_experience(exp: int) -> str
player.level_up() -> str
player.allocate_stat_point(stat: str) -> bool  # "attack", "defense", "hp", "mana"

# Economy
player.add_gold(amount: int) -> None
```

#### Enemy Methods
```python
# Drop system
enemy.add_drop(item: Item, chance: float) -> None  # chance: 0.0-1.0
enemy.get_drops() -> List[Item]

# AI
enemy.ai_choose_ability(target) -> Optional[Ability]
```

#### Shop Methods
```python
# Inventory management
shop.add_item(item: Item, quantity: int = 1) -> None
shop.remove_item(item_name: str) -> bool
shop.list_items() -> List[Item]

# Pricing
# Note: These are direct attribute assignments, not method calls

# Transactions
shop.buy_item(player: Player, item: Item) -> bool
shop.sell_item(player: Player, item: Item) -> bool
```

#### Ability Methods
```python
# Usage
ability.can_use(caster) -> bool
ability.use(caster, target=None) -> str
ability.reduce_cooldown() -> None
```

### Factory Method Reference

#### ItemFactory Methods
```python
ItemFactory.create_weapon(name: str, attack_bonus: int, value: int = None, description: str = "") -> Item
ItemFactory.create_armor(name: str, defense_bonus: int, value: int = None, description: str = "") -> Item
ItemFactory.create_consumable(name: str, value: int, description: str = "") -> Item
ItemFactory.create_health_potion(healing_power: int = 50) -> Item
ItemFactory.create_mana_potion(mana_power: int = 30) -> Item
```

#### AbilityFactory Methods
```python
# Basic ability creation
AbilityFactory.create_attack_ability(name: str, power: int, mana_cost: int = 0, cooldown: int = 0, description: str = "") -> Ability
AbilityFactory.create_heal_ability(name: str, power: int, mana_cost: int = 0, cooldown: int = 0, description: str = "") -> Ability
AbilityFactory.create_buff_ability(name: str, mana_cost: int = 0, cooldown: int = 0, description: str = "") -> Ability

# Status effect abilities
AbilityFactory.create_status_effect_ability(name: str, power: int, mana_cost: int, status_effect_type: StatusEffectType, effect_duration: int, effect_power: int, cooldown: int = 0, description: str = "") -> Ability

# Pre-made abilities
AbilityFactory.slash() -> Ability
AbilityFactory.fireball() -> Ability
AbilityFactory.heal() -> Ability
AbilityFactory.power_strike() -> Ability
AbilityFactory.poison_dart() -> Ability
AbilityFactory.flame_strike() -> Ability
AbilityFactory.ice_shard() -> Ability
AbilityFactory.stunning_blow() -> Ability
AbilityFactory.weakness_curse() -> Ability
AbilityFactory.armor_break() -> Ability
AbilityFactory.battle_cry() -> Ability
AbilityFactory.shield_wall() -> Ability
```

#### EnemyFactory Methods
```python
# Custom enemy creation
EnemyFactory.create_custom_enemy(name: str, hp: int, mana: int, attack: int, defense: int, level: int, exp_reward: int = None, gold_reward: int = None, abilities: list = None, drops: list = None) -> Enemy

# Pre-made enemies
EnemyFactory.goblin(level: int = 1) -> Enemy
EnemyFactory.orc(level: int = 3) -> Enemy
EnemyFactory.skeleton_mage(level: int = 4) -> Enemy
EnemyFactory.dragon(level: int = 10) -> Enemy
EnemyFactory.venomous_spider(level: int = 2) -> Enemy
EnemyFactory.frost_elemental(level: int = 5) -> Enemy
EnemyFactory.fire_demon(level: int = 6) -> Enemy
EnemyFactory.shadow_assassin(level: int = 7) -> Enemy
EnemyFactory.nature_shaman(level: int = 4) -> Enemy
```

#### ShopFactory Methods
```python
ShopFactory.create_weapon_shop() -> Shop
ShopFactory.create_armor_shop() -> Shop
ShopFactory.create_potion_shop() -> Shop
ShopFactory.create_general_shop() -> Shop
```

### Class Attributes Reference

#### Character Attributes
```python
character.name: str                    # Character name
character.hp: int                      # Current hit points
character.max_hp: int                  # Maximum hit points
character.mana: int                    # Current mana
character.max_mana: int                # Maximum mana
character.attack: int                  # Base attack power
character.defense: int                 # Base defense
character.abilities: List[Ability]     # List of known abilities
character.inventory: List[Item]        # Items in inventory
character.equipped: Dict[str, Item]    # Equipped items by slot
character.status_effects: List[StatusEffect]  # Active status effects
```

#### Player Attributes
```python
player.level: int                      # Current level
player.experience: int                 # Current experience points
player.experience_to_next_level: int   # EXP needed for next level
player.gold: int                       # Current gold amount
player.stat_points: int                # Unspent stat points
```

#### Enemy Attributes
```python
enemy.level: int                       # Enemy level
enemy.exp_reward: int                  # EXP given when defeated
enemy.gold_reward: int                 # Gold given when defeated
enemy.drop_table: List[Dict]           # Items that can be dropped
```

#### Item Attributes
```python
item.name: str                         # Item name
item.item_type: ItemType               # Type of item
item.value: int                        # Gold value
item.description: str                  # Item description
item.stats: Dict[str, int]             # Stat bonuses provided
```

#### Ability Attributes
```python
ability.name: str                      # Ability name
ability.ability_type: AbilityType      # Type of ability
ability.power: int                     # Damage or healing amount
ability.mana_cost: int                 # Mana required to use
ability.description: str               # Ability description
ability.cooldown: int                  # Turns between uses
ability.current_cooldown: int          # Current cooldown remaining
ability.status_effect: StatusEffect    # Status effect to apply (optional)
```

#### StatusEffect Attributes
```python
status_effect.name: str                # Effect name
status_effect.effect_type: StatusEffectType  # Type of effect
status_effect.duration: int            # Total duration in turns
status_effect.remaining_duration: int  # Turns remaining
status_effect.power: int               # Effect strength
status_effect.description: str         # Effect description
```

#### Shop Attributes
```python
shop.name: str                         # Shop name
shop.inventory: List[Item]             # Items for sale
shop.buy_price_multiplier: float       # Price multiplier for buying (default 1.0)
shop.sell_price_multiplier: float      # Price multiplier for selling (default 0.5)
```

Players gain experience and level up automatically:

```python
# Experience system
player.gain_experience(100)  # Returns level up message if leveled

# Each level increases stats and provides stat points
# Players can allocate stat points manually
player.allocate_stat_point("attack")
player.allocate_stat_point("defense")
player.allocate_stat_point("hp")
player.allocate_stat_point("mana")
```

## Example Usage

See `example_usage.py` for a complete demonstration of all features:

```bash
python example_usage.py
```

This will show:
- Player creation and leveling
- Enemy creation with custom abilities and drops
- Shop systems with item management
- Combat with abilities and AI
- Item equipment and stat bonuses

## File Structure

```
rpglib/
├── rpg_core.py      # Core classes (Player, Enemy, Item, Ability, Shop)
├── rpg_factory.py   # Factory classes for easy content creation
├── example_usage.py # Complete demonstration script
└── README.md        # This documentation
```

## Customization

The library is designed to be highly customizable:

- **Enemies**: Create custom enemies with any combination of stats, abilities, and drops
- **Items**: Define custom items with unique effects and bonuses
- **Abilities**: Create abilities with custom damage, effects, and cooldowns
- **Shops**: Set custom pricing and inventory for different shop types
- **Leveling**: Modify experience requirements and stat growth per level

## Getting Started

1. Copy the `rpg_core.py` and `rpg_factory.py` files to your project
2. Import the classes you need
3. Start creating your RPG system!

```python
from rpg_core import Player
from rpg_factory import EnemyFactory, ItemFactory

# Your RPG adventure begins here!
player = Player("Your Hero")
first_enemy = EnemyFactory.goblin()
```

## License

This library is provided as-is for educational and development purposes. Feel free to modify and extend it for your projects!