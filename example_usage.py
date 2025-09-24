"""
RPG Library Example Usage
=========================

This script demonstrates how to use the RPG library with all its features:
- Creating players with leveling system
- Creating customizable enemies with abilities and drops
- Setting up shops with easy item addition
- Combat system with abilities and status effects
- Item management and equipment
- Status effects and their interactions
"""

from rpg_core import Player, Shop, ItemType, AbilityType, StatusEffectType
from rpg_factory import ItemFactory, AbilityFactory, EnemyFactory, ShopFactory
import random


def demonstrate_player_creation():
    """Demonstrate player creation and leveling."""
    print("=== Player Creation and Leveling ===")
    
    # Create a player
    player = Player("Hero", hp=120, mana=60, attack=12, defense=6)
    print(f"Created player: {player.name}")
    print(f"Level: {player.level}, HP: {player.hp}/{player.max_hp}, MP: {player.mana}/{player.max_mana}")
    print(f"Attack: {player.attack}, Defense: {player.defense}")
    print(f"Experience: {player.experience}/{player.experience_to_next_level}")
    
    # Add some abilities to the player (including status effect abilities)
    player.add_ability(AbilityFactory.slash())
    player.add_ability(AbilityFactory.heal())
    player.add_ability(AbilityFactory.fireball())
    player.add_ability(AbilityFactory.poison_dart())
    player.add_ability(AbilityFactory.battle_cry())
    
    print(f"Added abilities: {[ability.name for ability in player.abilities]}")
    
    # Simulate gaining experience and leveling up
    print("\n--- Gaining Experience ---")
    for i in range(3):
        exp_gain = random.randint(80, 120)
        print(f"Gained {exp_gain} experience!")
        result = player.gain_experience(exp_gain)
        if result:
            print(result)
        print(f"Level: {player.level}, Experience: {player.experience}/{player.experience_to_next_level}")
    
    print()


def demonstrate_enemy_creation():
    """Demonstrate enemy creation with abilities and drops."""
    print("=== Enemy Creation and Customization ===")
    
    # Create enemies using factory
    goblin = EnemyFactory.goblin(level=2)
    orc = EnemyFactory.orc(level=4)
    dragon = EnemyFactory.dragon(level=8)
    
    enemies = [goblin, orc, dragon]
    
    for enemy in enemies:
        print(f"\n{enemy.name}:")
        print(f"  HP: {enemy.hp}, MP: {enemy.mana}")
        print(f"  Attack: {enemy.attack}, Defense: {enemy.defense}")
        print(f"  Abilities: {[ability.name for ability in enemy.abilities]}")
        print(f"  Rewards: {enemy.exp_reward} EXP, {enemy.gold_reward} Gold")
        print(f"  Drop Table: {len(enemy.drop_table)} possible drops")
    
    # Create a custom enemy
    print("\n--- Custom Enemy Creation ---")
    custom_abilities = [
        AbilityFactory.create_attack_ability("Shadow Strike", 20, 8, 1, "A dark energy attack"),
        AbilityFactory.heal()
    ]
    
    custom_drops = [
        (ItemFactory.create_weapon("Shadow Blade", 15, 200), 0.5),
        (ItemFactory.create_consumable("Dark Crystal", 100), 0.8)
    ]
    
    shadow_beast = EnemyFactory.create_custom_enemy(
        name="Shadow Beast",
        hp=80,
        mana=40,
        attack=18,
        defense=8,
        level=6,
        abilities=custom_abilities,
        drops=custom_drops
    )
    
    print(f"Created custom enemy: {shadow_beast.name}")
    print(f"  Abilities: {[ability.name for ability in shadow_beast.abilities]}")
    print(f"  Custom drops: {len(shadow_beast.drop_table)} items")
    
    print()


def demonstrate_shops():
    """Demonstrate shop system with easy item addition."""
    print("=== Shop System ===")
    
    # Create different types of shops
    weapon_shop = ShopFactory.create_weapon_shop()
    armor_shop = ShopFactory.create_armor_shop()
    potion_shop = ShopFactory.create_potion_shop()
    
    shops = [weapon_shop, armor_shop, potion_shop]
    
    for shop in shops:
        print(f"\n{shop.name}:")
        items = shop.list_items()
        for item in items[:3]:  # Show first 3 items
            print(f"  {item}")
        if len(items) > 3:
            print(f"  ... and {len(items) - 3} more items")
    
    # Create a custom shop and add items easily
    print("\n--- Custom Shop Creation ---")
    custom_shop = Shop("Rare Items Emporium")
    custom_shop.buy_price_multiplier = 1.5  # More expensive
    custom_shop.sell_price_multiplier = 0.7  # Better sell prices
    
    # Add custom items
    rare_items = [
        ItemFactory.create_weapon("Excalibur", 25, 1000, "Legendary sword"),
        ItemFactory.create_armor("Divine Shield", 20, 800, "Blessed protection"),
        ItemFactory.create_consumable("Elixir of Life", 500, "Grants temporary immortality")
    ]
    
    for item in rare_items:
        custom_shop.add_item(item)
    
    print(f"{custom_shop.name}:")
    for item_desc in custom_shop.list_items():
        print(f"  {item_desc}")
    
    print()


def demonstrate_combat():
    """Demonstrate combat system with abilities and status effects."""
    print("=== Combat System with Status Effects ===")
    
    # Create player and enemy
    player = Player("Warrior", hp=100, mana=50, attack=15, defense=8)
    player.add_ability(AbilityFactory.slash())
    player.add_ability(AbilityFactory.power_strike())
    player.add_ability(AbilityFactory.heal())
    player.add_ability(AbilityFactory.poison_dart())
    player.add_ability(AbilityFactory.battle_cry())
    player.add_gold(100)
    
    enemy = EnemyFactory.orc(level=3)
    
    print(f"Combat: {player.name} vs {enemy.name}")
    print(f"Player: {player.hp} HP, {player.mana} MP")
    print(f"Enemy: {enemy.hp} HP, {enemy.mana} MP")
    
    # Simulate a few rounds of combat
    round_num = 1
    while player.is_alive() and enemy.is_alive() and round_num <= 8:
        print(f"\n--- Round {round_num} ---")
        
        # Process status effects at the start of each round
        player.process_status_effects()
        enemy.process_status_effects()
        
        # Player turn
        if player.abilities and not player.has_status_effect(StatusEffectType.STUN):
            ability = random.choice(player.abilities)
            if ability.can_use(player):
                result = ability.use(player, enemy)
                print(result)
            else:
                print(f"{player.name} cannot use {ability.name}")
        elif player.has_status_effect(StatusEffectType.STUN):
            print(f"{player.name} is stunned and cannot act!")
        
        # Enemy turn (if still alive)
        if enemy.is_alive() and not enemy.has_status_effect(StatusEffectType.STUN):
            enemy_ability = enemy.ai_choose_ability(player)
            if enemy_ability:
                result = enemy_ability.use(enemy, player)
                print(result)
            else:
                # Basic attack if no abilities available
                damage = enemy.get_total_attack() + random.randint(-3, 3)
                actual_damage = player.take_damage(damage)
                print(f"{enemy.name} attacks {player.name} for {actual_damage} damage!")
        elif enemy.has_status_effect(StatusEffectType.STUN):
            print(f"{enemy.name} is stunned and cannot act!")
        
        # Update cooldowns
        player.update_cooldowns()
        enemy.update_cooldowns()
        
        # Show current status effects
        player_effects = [effect.effect_type.name for effect in player.status_effects]
        enemy_effects = [effect.effect_type.name for effect in enemy.status_effects]
        
        status_info = f"Player HP: {player.hp}/{player.max_hp}, Enemy HP: {enemy.hp}/{enemy.max_hp}"
        if player_effects:
            status_info += f" | Player Effects: {', '.join(player_effects)}"
        if enemy_effects:
            status_info += f" | Enemy Effects: {', '.join(enemy_effects)}"
        print(status_info)
        
        round_num += 1
    
    # Determine winner and rewards
    if not enemy.is_alive():
        print(f"\n{player.name} wins!")
        player.gain_experience(enemy.exp_reward)
        player.add_gold(enemy.gold_reward)
        print(f"Gained {enemy.exp_reward} EXP and {enemy.gold_reward} gold!")
        
        # Get drops
        drops = enemy.get_drops()
        if drops:
            print("Drops received:")
            for drop in drops:
                player.add_item(drop)
                print(f"  {drop.name}")
        else:
            print("No drops this time.")
    
    print()


def demonstrate_status_effects():
    """Demonstrate status effects in detail."""
    print("=== Status Effects Demonstration ===")
    
    # Create test characters
    player = Player("Mage", hp=80, mana=100, attack=10, defense=5)
    enemy = Player("Test Dummy", hp=100, mana=50, attack=8, defense=3)  # Using Player as test dummy
    
    # Add status effect abilities
    player.add_ability(AbilityFactory.poison_dart())
    player.add_ability(AbilityFactory.flame_strike())
    player.add_ability(AbilityFactory.ice_shard())
    player.add_ability(AbilityFactory.weakness_curse())
    player.add_ability(AbilityFactory.battle_cry())
    
    print(f"Testing status effects with {player.name} vs {enemy.name}")
    print(f"Initial stats - Player: {player.get_total_attack()} ATK, {player.get_total_defense()} DEF")
    print(f"Initial stats - Enemy: {enemy.get_total_attack()} ATK, {enemy.get_total_defense()} DEF")
    
    # Test different status effects
    status_abilities = [
        AbilityFactory.poison_dart(),
        AbilityFactory.flame_strike(),
        AbilityFactory.ice_shard(),
        AbilityFactory.weakness_curse(),
        AbilityFactory.battle_cry()
    ]
    
    for i, ability in enumerate(status_abilities):
        print(f"\n--- Testing {ability.name} ---")
        
        if ability.ability_type == AbilityType.BUFF:
            result = ability.use(player, player)  # Self-buff
        else:
            result = ability.use(player, enemy)
        
        print(result)
        
        # Show status effects
        if ability.ability_type == AbilityType.BUFF:
            effects = [f"{effect.effect_type.name} ({effect.duration} turns)" for effect in player.status_effects]
            if effects:
                print(f"Player status effects: {', '.join(effects)}")
                print(f"Modified stats - Player: {player.get_total_attack()} ATK, {player.get_total_defense()} DEF")
        else:
            effects = [f"{effect.effect_type.name} ({effect.duration} turns)" for effect in enemy.status_effects]
            if effects:
                print(f"Enemy status effects: {', '.join(effects)}")
                print(f"Modified stats - Enemy: {enemy.get_total_attack()} ATK, {enemy.get_total_defense()} DEF")
        
        # Process one turn of status effects
        print("Processing status effects...")
        player.process_status_effects()
        enemy.process_status_effects()
        
        print(f"After processing - Player HP: {player.hp}, Enemy HP: {enemy.hp}")
    
    print()


def demonstrate_item_management():
    """Demonstrate item management and equipment."""
    print("=== Item Management and Equipment ===")
    
    player = Player("Knight")
    
    # Create and add items
    sword = ItemFactory.create_weapon("Steel Sword", 10, 50)
    armor = ItemFactory.create_armor("Chain Mail", 5, 40)
    potion = ItemFactory.create_health_potion(50)
    
    player.add_item(sword)
    player.add_item(armor)
    player.add_item(potion)
    
    print(f"Player inventory: {[item.name for item in player.inventory]}")
    print(f"Base stats - Attack: {player.attack}, Defense: {player.defense}")
    
    # Equip items
    player.equip_item(sword, "weapon")
    player.equip_item(armor, "armor")
    
    print(f"After equipping items:")
    print(f"  Total Attack: {player.get_total_attack()}")
    print(f"  Total Defense: {player.get_total_defense()}")
    print(f"  Equipped: {list(player.equipped.keys())}")
    print(f"  Inventory: {[item.name for item in player.inventory]}")
    
    print()


def main():
    """Run all demonstrations."""
    print("RPG Library Demonstration")
    print("=" * 50)
    
    demonstrate_player_creation()
    demonstrate_enemy_creation()
    demonstrate_shops()
    demonstrate_status_effects()
    demonstrate_combat()
    demonstrate_item_management()
    
    print("=" * 50)
    print("Demonstration complete! The RPG library supports:")
    print("✓ Player creation and leveling")
    print("✓ Customizable enemies with abilities and drops")
    print("✓ Shop system with easy item management")
    print("✓ Status effects and abilities that inflict them")
    print("✓ Combat system with status effect interactions")
    print("✓ Item management and equipment system")
    print("✓ Easy factory classes for quick content creation")


if __name__ == "__main__":
    main()