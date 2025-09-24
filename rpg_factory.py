"""
RPG Factory Module
==================

This module provides easy-to-use factory functions for creating common RPG elements
like items, abilities, and enemies. This makes it simple to add new content to your game.
"""

from rpg_core import Item, ItemType, Ability, AbilityType, Enemy, Player, StatusEffect, StatusEffectType
import random


class ItemFactory:
    """Factory class for creating common items."""
    
    @staticmethod
    def create_weapon(name: str, attack_bonus: int, value: int = None, description: str = ""):
        """Create a weapon item."""
        if value is None:
            value = attack_bonus * 10
        return Item(
            name=name,
            item_type=ItemType.WEAPON,
            value=value,
            description=description,
            stats={"attack": attack_bonus}
        )
    
    @staticmethod
    def create_armor(name: str, defense_bonus: int, value: int = None, description: str = ""):
        """Create an armor item."""
        if value is None:
            value = defense_bonus * 8
        return Item(
            name=name,
            item_type=ItemType.ARMOR,
            value=value,
            description=description,
            stats={"defense": defense_bonus}
        )
    
    @staticmethod
    def create_consumable(name: str, value: int, description: str = ""):
        """Create a consumable item."""
        return Item(
            name=name,
            item_type=ItemType.CONSUMABLE,
            value=value,
            description=description
        )
    
    @staticmethod
    def create_health_potion(healing_power: int = 50):
        """Create a health potion."""
        return Item(
            name=f"Health Potion ({healing_power} HP)",
            item_type=ItemType.CONSUMABLE,
            value=healing_power // 2,
            description=f"Restores {healing_power} HP when consumed",
            stats={"heal": healing_power}
        )
    
    @staticmethod
    def create_mana_potion(mana_power: int = 30):
        """Create a mana potion."""
        return Item(
            name=f"Mana Potion ({mana_power} MP)",
            item_type=ItemType.CONSUMABLE,
            value=mana_power // 2,
            description=f"Restores {mana_power} MP when consumed",
            stats={"mana": mana_power}
        )


class AbilityFactory:
    """Factory class for creating common abilities."""
    
    @staticmethod
    def create_attack_ability(name: str, power: int, mana_cost: int = 0, 
                            cooldown: int = 0, description: str = ""):
        """Create an attack ability."""
        return Ability(
            name=name,
            ability_type=AbilityType.ATTACK,
            power=power,
            mana_cost=mana_cost,
            description=description,
            cooldown=cooldown
        )
    
    @staticmethod
    def create_heal_ability(name: str, power: int, mana_cost: int, 
                          cooldown: int = 0, description: str = ""):
        """Create a healing ability."""
        return Ability(
            name=name,
            ability_type=AbilityType.HEAL,
            power=power,
            mana_cost=mana_cost,
            description=description,
            cooldown=cooldown
        )
    
    @staticmethod
    def create_buff_ability(name: str, mana_cost: int, cooldown: int = 0, 
                          description: str = ""):
        """Create a buff ability."""
        return Ability(
            name=name,
            ability_type=AbilityType.BUFF,
            power=0,
            mana_cost=mana_cost,
            description=description,
            cooldown=cooldown
        )
    
    @staticmethod
    def create_status_effect_ability(name: str, power: int, mana_cost: int, 
                                   status_effect_type: StatusEffectType, 
                                   effect_duration: int, effect_power: int = 0,
                                   cooldown: int = 0, description: str = ""):
        """Create an ability that inflicts a status effect."""
        # Create the status effect object
        status_effect = StatusEffect(
            name=f"{name} Effect",
            effect_type=status_effect_type,
            duration=effect_duration,
            power=effect_power,
            description=f"Status effect from {name}"
        )
        
        ability = Ability(
            name=name,
            ability_type=AbilityType.ATTACK,
            power=power,
            mana_cost=mana_cost,
            description=description,
            cooldown=cooldown,
            status_effect=status_effect
        )
        return ability
    
    # Predefined common abilities
    @staticmethod
    def slash():
        """Basic sword slash attack."""
        return AbilityFactory.create_attack_ability(
            "Slash", 15, 0, 0, "A basic sword attack"
        )
    
    @staticmethod
    def fireball():
        """Fireball spell."""
        return AbilityFactory.create_attack_ability(
            "Fireball", 25, 10, 1, "A magical fireball attack"
        )
    
    @staticmethod
    def heal():
        """Basic heal spell."""
        return AbilityFactory.create_heal_ability(
            "Heal", 30, 8, 0, "Restores health"
        )
    
    @staticmethod
    def power_strike():
        """Powerful melee attack."""
        return AbilityFactory.create_attack_ability(
            "Power Strike", 35, 5, 2, "A devastating melee attack"
        )
    
    # Status effect abilities
    @staticmethod
    def poison_dart():
        """Poison dart attack that inflicts poison."""
        return AbilityFactory.create_status_effect_ability(
            "Poison Dart", 10, 8, StatusEffectType.POISON, 3, 5, 1,
            "A dart coated with poison that deals damage over time"
        )
    
    @staticmethod
    def flame_strike():
        """Fire attack that inflicts burn."""
        return AbilityFactory.create_status_effect_ability(
            "Flame Strike", 20, 12, StatusEffectType.BURN, 3, 8, 2,
            "A fiery attack that burns the target"
        )
    
    @staticmethod
    def ice_shard():
        """Ice attack that can freeze the target."""
        return AbilityFactory.create_status_effect_ability(
            "Ice Shard", 15, 10, StatusEffectType.FREEZE, 2, 0, 2,
            "An icy projectile that can freeze enemies"
        )
    
    @staticmethod
    def stunning_blow():
        """Physical attack that can stun."""
        return AbilityFactory.create_status_effect_ability(
            "Stunning Blow", 18, 6, StatusEffectType.STUN, 1, 0, 3,
            "A powerful blow that can stun the target"
        )
    
    @staticmethod
    def weakness_curse():
        """Curse that reduces enemy attack."""
        return AbilityFactory.create_status_effect_ability(
            "Weakness Curse", 5, 15, StatusEffectType.WEAKNESS, 4, 10, 1,
            "A curse that weakens the enemy's attack power"
        )
    
    @staticmethod
    def armor_break():
        """Attack that reduces enemy defense."""
        return AbilityFactory.create_status_effect_ability(
            "Armor Break", 12, 8, StatusEffectType.VULNERABILITY, 3, 8, 2,
            "An attack that breaks through armor, reducing defense"
        )
    
    @staticmethod
    def battle_cry():
        """Buff that increases own attack."""
        ability = AbilityFactory.create_status_effect_ability(
            "Battle Cry", 0, 10, StatusEffectType.STRENGTH_BOOST, 5, 15, 3,
            "A rallying cry that boosts attack power"
        )
        ability.ability_type = AbilityType.BUFF
        return ability
    
    @staticmethod
    def shield_wall():
        """Buff that increases own defense."""
        ability = AbilityFactory.create_status_effect_ability(
            "Shield Wall", 0, 12, StatusEffectType.DEFENSE_BOOST, 4, 12, 2,
            "A defensive stance that increases defense"
        )
        ability.ability_type = AbilityType.BUFF
        return ability


class EnemyFactory:
    """Factory class for creating common enemy types."""
    
    @staticmethod
    def create_custom_enemy(name: str, hp: int, mana: int, attack: int, 
                          defense: int, level: int, exp_reward: int = None, 
                          gold_reward: int = None, abilities: list = None, 
                          drops: list = None):
        """Create a fully customizable enemy."""
        if exp_reward is None:
            exp_reward = level * 20 + random.randint(5, 15)
        if gold_reward is None:
            gold_reward = level * 8 + random.randint(2, 8)
        
        enemy = Enemy(name, hp, mana, attack, defense, level, exp_reward, gold_reward)
        
        # Add abilities
        if abilities:
            for ability in abilities:
                enemy.add_ability(ability)
        
        # Add drops
        if drops:
            for item, chance in drops:
                enemy.add_drop(item, chance)
        
        return enemy
    
    @staticmethod
    def goblin(level: int = 1):
        """Create a goblin enemy."""
        base_hp = 30 + (level - 1) * 8
        base_attack = 6 + (level - 1) * 2
        base_defense = 2 + (level - 1)
        
        goblin = EnemyFactory.create_custom_enemy(
            name=f"Goblin (Lv.{level})",
            hp=base_hp,
            mana=10,
            attack=base_attack,
            defense=base_defense,
            level=level,
            abilities=[
                AbilityFactory.slash(), 
                AbilityFactory.poison_dart(),
                AbilityFactory.create_status_effect_ability(
                    "Dirty Fighting", 8, 4, StatusEffectType.WEAKNESS, 2, 5, 2,
                    "A sneaky attack that weakens the opponent"
                )
            ],
            drops=[
                (ItemFactory.create_weapon("Rusty Dagger", 3, 15), 0.3),
                (ItemFactory.create_consumable("Goblin Ear", 5), 0.8),
                (ItemFactory.create_health_potion(25), 0.2)
            ]
        )
        return goblin
    
    @staticmethod
    def orc(level: int = 3):
        """Create an orc enemy."""
        base_hp = 60 + (level - 1) * 12
        base_attack = 12 + (level - 1) * 3
        base_defense = 5 + (level - 1) * 2
        
        orc = EnemyFactory.create_custom_enemy(
            name=f"Orc Warrior (Lv.{level})",
            hp=base_hp,
            mana=20,
            attack=base_attack,
            defense=base_defense,
            level=level,
            abilities=[
                AbilityFactory.slash(), 
                AbilityFactory.power_strike(), 
                AbilityFactory.stunning_blow(),
                AbilityFactory.create_status_effect_ability(
                    "Berserker Rage", 0, 8, StatusEffectType.STRENGTH_BOOST, 3, 12, 4,
                    "Enters a rage that increases attack power"
                )
            ],
            drops=[
                (ItemFactory.create_weapon("Orcish Axe", 8, 50), 0.4),
                (ItemFactory.create_armor("Leather Armor", 4, 40), 0.3),
                (ItemFactory.create_health_potion(50), 0.5)
            ]
        )
        return orc
    
    @staticmethod
    def skeleton_mage(level: int = 4):
        """Create a skeleton mage enemy."""
        base_hp = 40 + (level - 1) * 6
        base_attack = 8 + (level - 1) * 2
        base_defense = 3 + (level - 1)
        base_mana = 40 + (level - 1) * 5
        
        skeleton = EnemyFactory.create_custom_enemy(
            name=f"Skeleton Mage (Lv.{level})",
            hp=base_hp,
            mana=base_mana,
            attack=base_attack,
            defense=base_defense,
            level=level,
            abilities=[
                AbilityFactory.fireball(), 
                AbilityFactory.heal(), 
                AbilityFactory.ice_shard(), 
                AbilityFactory.weakness_curse(),
                AbilityFactory.create_status_effect_ability(
                    "Bone Chill", 12, 6, StatusEffectType.FREEZE, 2, 8, 3,
                    "A chilling spell that slows the enemy"
                ),
                AbilityFactory.create_status_effect_ability(
                    "Dark Ritual", 0, 15, StatusEffectType.REGENERATION, 3, 10, 5,
                    "Channels dark magic to regenerate health"
                )
            ],
            drops=[
                (ItemFactory.create_weapon("Magic Staff", 6, 60), 0.3),
                (ItemFactory.create_mana_potion(40), 0.6),
                (ItemFactory.create_consumable("Bone Fragment", 8), 0.9)
            ]
        )
        return skeleton
    
    @staticmethod
    def dragon(level: int = 10):
        """Create a dragon boss enemy."""
        base_hp = 200 + (level - 1) * 25
        base_attack = 25 + (level - 1) * 4
        base_defense = 15 + (level - 1) * 3
        base_mana = 80 + (level - 1) * 8
        
        dragon = EnemyFactory.create_custom_enemy(
            name=f"Ancient Dragon (Lv.{level})",
            hp=base_hp,
            mana=base_mana,
            attack=base_attack,
            defense=base_defense,
            level=level,
            exp_reward=level * 100,
            gold_reward=level * 50,
            abilities=[
                AbilityFactory.create_attack_ability("Dragon Breath", 45, 15, 3, "Devastating fire breath"),
                AbilityFactory.create_attack_ability("Claw Strike", 30, 0, 1, "Powerful claw attack"),
                AbilityFactory.fireball(),
                AbilityFactory.flame_strike(),
                AbilityFactory.armor_break(),
                AbilityFactory.create_status_effect_ability(
                    "Dragon's Roar", 15, 8, StatusEffectType.STUN, 1, 15, 6,
                    "A terrifying roar that stuns enemies with fear"
                ),
                AbilityFactory.create_status_effect_ability(
                    "Molten Scales", 0, 20, StatusEffectType.DEFENSE_BOOST, 4, 12, 8,
                    "Hardens scales to increase defense"
                )
            ],
            drops=[
                (ItemFactory.create_weapon("Dragon Sword", 20, 500), 0.8),
                (ItemFactory.create_armor("Dragon Scale Armor", 15, 400), 0.7),
                (ItemFactory.create_consumable("Dragon Heart", 1000), 1.0),
                (ItemFactory.create_health_potion(100), 0.9)
            ]
        )
        return dragon
    
    @staticmethod
    def venomous_spider(level: int = 2):
        """Create a venomous spider enemy that specializes in poison effects."""
        base_hp = 25 + (level - 1) * 5
        base_attack = 8 + (level - 1) * 2
        base_defense = 3 + (level - 1)
        base_mana = 15 + (level - 1) * 3
        
        spider = EnemyFactory.create_custom_enemy(
            name=f"Venomous Spider (Lv.{level})",
            hp=base_hp,
            mana=base_mana,
            attack=base_attack,
            defense=base_defense,
            level=level,
            abilities=[
                AbilityFactory.poison_dart(),
                AbilityFactory.create_status_effect_ability(
                    "Venom Bite", 12, 5, StatusEffectType.POISON, 4, 8, 1,
                    "A venomous bite that causes severe poisoning"
                ),
                AbilityFactory.weakness_curse()
            ],
            drops=[
                (ItemFactory.create_consumable("Spider Venom", 25), 0.7),
                (ItemFactory.create_consumable("Spider Silk", 15), 0.9),
                (ItemFactory.create_health_potion(25), 0.3)
            ]
        )
        return spider
    
    @staticmethod
    def frost_elemental(level: int = 5):
        """Create a frost elemental enemy that specializes in freeze effects."""
        base_hp = 70 + (level - 1) * 10
        base_attack = 10 + (level - 1) * 2
        base_defense = 8 + (level - 1) * 2
        base_mana = 60 + (level - 1) * 8
        
        elemental = EnemyFactory.create_custom_enemy(
            name=f"Frost Elemental (Lv.{level})",
            hp=base_hp,
            mana=base_mana,
            attack=base_attack,
            defense=base_defense,
            level=level,
            abilities=[
                AbilityFactory.ice_shard(),
                AbilityFactory.create_status_effect_ability(
                    "Frost Aura", 8, 12, StatusEffectType.FREEZE, 2, 0, 2,
                    "An aura of cold that can freeze enemies solid"
                ),
                AbilityFactory.create_status_effect_ability(
                    "Ice Prison", 5, 15, StatusEffectType.STUN, 2, 0, 3,
                    "Encases the target in ice, preventing movement"
                )
            ],
            drops=[
                (ItemFactory.create_consumable("Frost Crystal", 40), 0.6),
                (ItemFactory.create_mana_potion(50), 0.5),
                (ItemFactory.create_weapon("Ice Shard", 7, 45), 0.4)
            ]
        )
        return elemental
    
    @staticmethod
    def fire_demon(level: int = 6):
        """Create a fire demon enemy that specializes in burn effects."""
        base_hp = 80 + (level - 1) * 12
        base_attack = 14 + (level - 1) * 3
        base_defense = 6 + (level - 1) * 2
        base_mana = 50 + (level - 1) * 6
        
        demon = EnemyFactory.create_custom_enemy(
            name=f"Fire Demon (Lv.{level})",
            hp=base_hp,
            mana=base_mana,
            attack=base_attack,
            defense=base_defense,
            level=level,
            abilities=[
                AbilityFactory.flame_strike(),
                AbilityFactory.fireball(),
                AbilityFactory.create_status_effect_ability(
                    "Inferno", 25, 18, StatusEffectType.BURN, 4, 12, 3,
                    "A devastating fire attack that burns for extended periods"
                ),
                AbilityFactory.armor_break()
            ],
            drops=[
                (ItemFactory.create_weapon("Flame Sword", 12, 80), 0.5),
                (ItemFactory.create_consumable("Demon Horn", 60), 0.8),
                (ItemFactory.create_health_potion(75), 0.4)
            ]
        )
        return demon
    
    @staticmethod
    def shadow_assassin(level: int = 7):
        """Create a shadow assassin enemy that specializes in debuffs and stuns."""
        base_hp = 60 + (level - 1) * 8
        base_attack = 16 + (level - 1) * 3
        base_defense = 4 + (level - 1)
        base_mana = 40 + (level - 1) * 5
        
        assassin = EnemyFactory.create_custom_enemy(
            name=f"Shadow Assassin (Lv.{level})",
            hp=base_hp,
            mana=base_mana,
            attack=base_attack,
            defense=base_defense,
            level=level,
            abilities=[
                AbilityFactory.stunning_blow(),
                AbilityFactory.weakness_curse(),
                AbilityFactory.create_status_effect_ability(
                    "Shadow Strike", 20, 10, StatusEffectType.VULNERABILITY, 3, 10, 2,
                    "A strike from the shadows that leaves the target vulnerable"
                ),
                AbilityFactory.create_status_effect_ability(
                    "Paralyzing Dart", 8, 12, StatusEffectType.STUN, 2, 0, 3,
                    "A dart that paralyzes the target temporarily"
                )
            ],
            drops=[
                (ItemFactory.create_weapon("Shadow Blade", 14, 120), 0.6),
                (ItemFactory.create_consumable("Shadow Essence", 50), 0.7),
                (ItemFactory.create_armor("Shadow Cloak", 6, 90), 0.4)
            ]
        )
        return assassin
    
    @staticmethod
    def nature_shaman(level: int = 4):
        """Create a nature shaman enemy that uses regeneration and buffs."""
        base_hp = 55 + (level - 1) * 9
        base_attack = 9 + (level - 1) * 2
        base_defense = 7 + (level - 1) * 2
        base_mana = 70 + (level - 1) * 10
        
        shaman = EnemyFactory.create_custom_enemy(
            name=f"Nature Shaman (Lv.{level})",
            hp=base_hp,
            mana=base_mana,
            attack=base_attack,
            defense=base_defense,
            level=level,
            abilities=[
                AbilityFactory.heal(),
                AbilityFactory.create_status_effect_ability(
                    "Nature's Blessing", 0, 15, StatusEffectType.REGENERATION, 5, 8, 2,
                    "Calls upon nature to heal over time"
                ),
                AbilityFactory.create_status_effect_ability(
                    "Bark Skin", 0, 12, StatusEffectType.DEFENSE_BOOST, 4, 10, 3,
                    "Hardens skin like tree bark for increased defense"
                ),
                AbilityFactory.weakness_curse()
            ],
            drops=[
                (ItemFactory.create_weapon("Nature Staff", 8, 65), 0.5),
                (ItemFactory.create_consumable("Healing Herbs", 30), 0.8),
                (ItemFactory.create_mana_potion(60), 0.6)
            ]
        )
        return shaman


class ShopFactory:
    """Factory class for creating pre-stocked shops."""
    
    @staticmethod
    def create_weapon_shop():
        """Create a weapon shop with various weapons."""
        from rpg_core import Shop
        
        shop = Shop("Blacksmith's Forge")
        
        # Add various weapons
        weapons = [
            ItemFactory.create_weapon("Iron Sword", 8, 40, "A sturdy iron sword"),
            ItemFactory.create_weapon("Steel Sword", 12, 80, "A sharp steel blade"),
            ItemFactory.create_weapon("Silver Dagger", 6, 60, "A quick silver dagger"),
            ItemFactory.create_weapon("War Hammer", 15, 120, "A heavy war hammer"),
            ItemFactory.create_weapon("Magic Staff", 10, 100, "A staff imbued with magic")
        ]
        
        for weapon in weapons:
            shop.add_item(weapon, random.randint(1, 3))
        
        return shop
    
    @staticmethod
    def create_armor_shop():
        """Create an armor shop with various armor pieces."""
        from rpg_core import Shop
        
        shop = Shop("Armor Emporium")
        
        # Add various armor
        armors = [
            ItemFactory.create_armor("Leather Armor", 3, 30, "Basic leather protection"),
            ItemFactory.create_armor("Chain Mail", 6, 60, "Flexible chain mail armor"),
            ItemFactory.create_armor("Plate Armor", 10, 150, "Heavy plate armor"),
            ItemFactory.create_armor("Mage Robes", 4, 80, "Robes that enhance magic"),
            ItemFactory.create_armor("Dragon Scale Vest", 12, 300, "Armor made from dragon scales")
        ]
        
        for armor in armors:
            shop.add_item(armor, random.randint(1, 2))
        
        return shop
    
    @staticmethod
    def create_potion_shop():
        """Create a potion shop with various consumables."""
        from rpg_core import Shop
        
        shop = Shop("Alchemist's Corner")
        
        # Add various potions
        potions = [
            ItemFactory.create_health_potion(25),
            ItemFactory.create_health_potion(50),
            ItemFactory.create_health_potion(100),
            ItemFactory.create_mana_potion(20),
            ItemFactory.create_mana_potion(40),
            ItemFactory.create_mana_potion(80)
        ]
        
        for potion in potions:
            shop.add_item(potion, random.randint(3, 8))
        
        return shop