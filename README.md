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
from rpg_factory import ItemFactory, AbilityFactory, EnemyFactory

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

### Player

The main character class with leveling and progression.

```python
player = Player("Hero", hp=100, mana=50, attack=10, defense=5)

# Leveling system
player.gain_experience(100)  # Automatically levels up when enough EXP

# Equipment system
sword = ItemFactory.create_weapon("Steel Sword", 10, 50)
player.add_item(sword)
player.equip_item(sword, "weapon")

# Abilities
player.add_ability(AbilityFactory.fireball())
player.use_ability("Fireball", target)
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

# AI system
chosen_ability = enemy.ai_choose_ability(player)
drops = enemy.get_drops()  # Random drops based on drop table
```

### Shop

Easy shop creation and management.

```python
# Pre-made shops
weapon_shop = ShopFactory.create_weapon_shop()
armor_shop = ShopFactory.create_armor_shop()

# Custom shops
custom_shop = Shop("Magic Items")
custom_shop.add_item(ItemFactory.create_weapon("Magic Sword", 20, 200))

# Shopping
items = shop.list_items()
shop.sell_to_player(player, "Magic Sword")
shop.buy_from_player(player, old_sword)
```

## Factory Classes

### ItemFactory

Create various types of items easily:

```python
# Weapons
sword = ItemFactory.create_weapon("Steel Sword", attack_bonus=10, price=50)
bow = ItemFactory.create_weapon("Longbow", attack_bonus=8, price=40, description="Ranged weapon")

# Armor
armor = ItemFactory.create_armor("Chain Mail", defense_bonus=5, price=60)
shield = ItemFactory.create_armor("Iron Shield", defense_bonus=3, price=30)

# Consumables
health_potion = ItemFactory.create_health_potion(healing_amount=50)
mana_potion = ItemFactory.create_mana_potion(mana_amount=30)
custom_potion = ItemFactory.create_consumable("Super Potion", price=100, description="Heals everything")
```

### AbilityFactory

Create abilities with different effects:

```python
# Attack abilities
slash = AbilityFactory.slash()  # Basic attack
fireball = AbilityFactory.fireball()  # Magic attack
power_strike = AbilityFactory.power_strike()  # Strong physical attack

# Healing abilities
heal = AbilityFactory.heal()  # Basic healing

# Buff abilities
strength_boost = AbilityFactory.strength_boost()  # Temporary attack increase

# Custom abilities
custom_ability = AbilityFactory.create_attack_ability(
    name="Lightning Bolt",
    damage=25,
    mana_cost=15,
    cooldown=3,
    description="Strikes with lightning"
)
```

### EnemyFactory

Create enemies with predefined stats and abilities:

```python
# Common enemies
goblin = EnemyFactory.goblin(level=1)
orc = EnemyFactory.orc(level=3)
skeleton_mage = EnemyFactory.skeleton_mage(level=4)
dragon = EnemyFactory.dragon(level=10)

# Custom enemy with specific configuration
boss = EnemyFactory.create_custom_enemy(
    name="Dark Lord",
    hp=200, mana=100, attack=25, defense=15,
    level=15,
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

## Combat System

The library includes a flexible combat system:

```python
# Basic combat flow
if ability.can_use(player):
    result = ability.use(player, enemy)
    print(result)

# Enemy AI chooses abilities automatically
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

## Leveling and Experience

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