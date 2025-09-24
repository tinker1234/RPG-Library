"""
RPG Library Core Classes
========================

This module contains the core classes for an RPG system including:
- Character (base class for Player and Enemy)
- Player (with leveling system)
- Enemy (with customizable attributes and abilities)
- Item (equipment, consumables, etc.)
- Ability (skills, spells, attacks)
- Shop (for buying/selling items)
"""

import random
from typing import List, Dict, Optional, Any
from enum import Enum


class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    MISC = "misc"


class AbilityType(Enum):
    ATTACK = "attack"
    HEAL = "heal"
    BUFF = "buff"
    DEBUFF = "debuff"


class StatusEffectType(Enum):
    POISON = "poison"
    BURN = "burn"
    FREEZE = "freeze"
    STUN = "stun"
    STRENGTH_BOOST = "strength_boost"
    DEFENSE_BOOST = "defense_boost"
    SPEED_BOOST = "speed_boost"
    WEAKNESS = "weakness"
    VULNERABILITY = "vulnerability"
    REGENERATION = "regeneration"


class StatusEffect:
    """Represents a status effect that can be applied to characters."""
    
    def __init__(self, name: str, effect_type: StatusEffectType, duration: int,
                 power: int = 0, description: str = ""):
        self.name = name
        self.effect_type = effect_type
        self.duration = duration
        self.power = power
        self.description = description
        self.remaining_duration = duration
    
    def apply_effect(self, character) -> str:
        """Apply the status effect to a character each turn."""
        if self.remaining_duration <= 0:
            return ""
        
        result = ""
        
        if self.effect_type == StatusEffectType.POISON:
            damage = self.power
            character.take_damage(damage)
            result = f"{character.name} takes {damage} poison damage!"
        
        elif self.effect_type == StatusEffectType.BURN:
            damage = self.power
            character.take_damage(damage)
            result = f"{character.name} takes {damage} burn damage!"
        
        elif self.effect_type == StatusEffectType.REGENERATION:
            heal_amount = self.power
            character.heal(heal_amount)
            result = f"{character.name} regenerates {heal_amount} HP!"
        
        elif self.effect_type == StatusEffectType.FREEZE:
            result = f"{character.name} is frozen and cannot act!"
        
        elif self.effect_type == StatusEffectType.STUN:
            result = f"{character.name} is stunned and cannot act!"
        
        # Stat modification effects are handled in get_total_* methods
        elif self.effect_type in [StatusEffectType.STRENGTH_BOOST, StatusEffectType.WEAKNESS,
                                  StatusEffectType.DEFENSE_BOOST, StatusEffectType.VULNERABILITY]:
            result = f"{character.name} is affected by {self.name}!"
        
        self.remaining_duration -= 1
        return result
    
    def is_expired(self) -> bool:
        """Check if the status effect has expired."""
        return self.remaining_duration <= 0
    
    def prevents_action(self) -> bool:
        """Check if this status effect prevents the character from acting."""
        return self.effect_type in [StatusEffectType.FREEZE, StatusEffectType.STUN]
    
    def get_stat_modifier(self, stat: str) -> int:
        """Get the stat modifier for this effect."""
        if self.effect_type == StatusEffectType.STRENGTH_BOOST and stat == "attack":
            return self.power
        elif self.effect_type == StatusEffectType.WEAKNESS and stat == "attack":
            return -self.power
        elif self.effect_type == StatusEffectType.DEFENSE_BOOST and stat == "defense":
            return self.power
        elif self.effect_type == StatusEffectType.VULNERABILITY and stat == "defense":
            return -self.power
        return 0
    
    def __str__(self):
        return f"{self.name} ({self.remaining_duration} turns remaining)"


class Item:
    """Represents an item in the RPG system."""
    
    def __init__(self, name: str, item_type: ItemType, value: int = 0, 
                 description: str = "", stats: Dict[str, int] = None):
        self.name = name
        self.item_type = item_type
        self.value = value  # Gold value
        self.description = description
        self.stats = stats or {}  # e.g., {"attack": 10, "defense": 5}
    
    def __str__(self):
        return f"{self.name} ({self.item_type.value}) - {self.description}"


class Ability:
    """Represents an ability/skill that can be used by characters."""
    
    def __init__(self, name: str, ability_type: AbilityType, power: int = 0,
                 mana_cost: int = 0, description: str = "", cooldown: int = 0,
                 status_effect: StatusEffect = None):
        self.name = name
        self.ability_type = ability_type
        self.power = power
        self.mana_cost = mana_cost
        self.description = description
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.status_effect = status_effect  # Status effect to apply
    
    def can_use(self, caster) -> bool:
        """Check if the ability can be used by the caster."""
        return (self.current_cooldown == 0 and 
                caster.mana >= self.mana_cost and
                not caster.is_action_prevented())
    
    def use(self, caster, target=None):
        """Use the ability. Returns the result of the ability."""
        if not self.can_use(caster):
            if caster.is_action_prevented():
                return f"{caster.name} is unable to act!"
            return f"{caster.name} cannot use {self.name}!"
        
        caster.mana -= self.mana_cost
        self.current_cooldown = self.cooldown
        result_messages = []
        
        if self.ability_type == AbilityType.ATTACK:
            if target:
                damage = caster.get_total_attack() + self.power + random.randint(-5, 5)
                actual_damage = target.take_damage(damage)
                result_messages.append(f"{caster.name} attacks {target.name} with {self.name} for {actual_damage} damage!")
                
                # Apply status effect if any
                if self.status_effect and target.is_alive():
                    # Create a new instance of the status effect
                    new_effect = StatusEffect(
                        self.status_effect.name,
                        self.status_effect.effect_type,
                        self.status_effect.duration,
                        self.status_effect.power,
                        self.status_effect.description
                    )
                    target.add_status_effect(new_effect)
                    result_messages.append(f"{target.name} is affected by {new_effect.name}!")
        
        elif self.ability_type == AbilityType.HEAL:
            heal_amount = self.power + random.randint(-2, 2)
            caster.heal(heal_amount)
            result_messages.append(f"{caster.name} heals for {heal_amount} HP!")
            
            # Apply beneficial status effect if any
            if self.status_effect:
                new_effect = StatusEffect(
                    self.status_effect.name,
                    self.status_effect.effect_type,
                    self.status_effect.duration,
                    self.status_effect.power,
                    self.status_effect.description
                )
                caster.add_status_effect(new_effect)
                result_messages.append(f"{caster.name} gains {new_effect.name}!")
        
        elif self.ability_type == AbilityType.BUFF:
            if self.status_effect:
                new_effect = StatusEffect(
                    self.status_effect.name,
                    self.status_effect.effect_type,
                    self.status_effect.duration,
                    self.status_effect.power,
                    self.status_effect.description
                )
                target_char = target if target else caster
                target_char.add_status_effect(new_effect)
                result_messages.append(f"{target_char.name} gains {new_effect.name}!")
            else:
                result_messages.append(f"{caster.name} uses {self.name}!")
        
        elif self.ability_type == AbilityType.DEBUFF:
            if target and self.status_effect:
                new_effect = StatusEffect(
                    self.status_effect.name,
                    self.status_effect.effect_type,
                    self.status_effect.duration,
                    self.status_effect.power,
                    self.status_effect.description
                )
                target.add_status_effect(new_effect)
                result_messages.append(f"{target.name} is afflicted with {new_effect.name}!")
            else:
                result_messages.append(f"{caster.name} uses {self.name}!")
        
        return " ".join(result_messages)
    
    def reduce_cooldown(self):
        """Reduce cooldown by 1 (call each turn)."""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1


class Character:
    """Base class for all characters (Player and Enemy)."""
    
    def __init__(self, name: str, hp: int = 100, mana: int = 50, 
                 attack: int = 10, defense: int = 5):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mana = mana
        self.mana = mana
        self.attack = attack
        self.defense = defense
        self.abilities: List[Ability] = []
        self.inventory: List[Item] = []
        self.equipped: Dict[str, Item] = {}
        self.status_effects: List[StatusEffect] = []
    
    def add_ability(self, ability: Ability):
        """Add an ability to the character."""
        self.abilities.append(ability)
    
    def add_item(self, item: Item):
        """Add an item to inventory."""
        self.inventory.append(item)
    
    def equip_item(self, item: Item, slot: str = None):
        """Equip an item."""
        if item in self.inventory:
            if slot is None:
                slot = item.item_type.value
            
            # Unequip current item if any
            if slot in self.equipped:
                self.unequip_item(slot)
            
            self.equipped[slot] = item
            self.inventory.remove(item)
            
            # Apply item stats
            for stat, value in item.stats.items():
                if hasattr(self, stat):
                    setattr(self, stat, getattr(self, stat) + value)
    
    def unequip_item(self, slot: str):
        """Unequip an item from a slot."""
        if slot in self.equipped:
            item = self.equipped[slot]
            del self.equipped[slot]
            self.inventory.append(item)
            
            # Remove item stats
            for stat, value in item.stats.items():
                if hasattr(self, stat):
                    setattr(self, stat, getattr(self, stat) - value)
    
    def take_damage(self, damage: int):
        """Take damage, reduced by defense."""
        actual_damage = max(1, damage - self.get_total_defense())
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount: int):
        """Heal HP."""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def restore_mana(self, amount: int):
        """Restore mana."""
        self.mana = min(self.max_mana, self.mana + amount)
    
    def is_alive(self) -> bool:
        """Check if character is alive."""
        return self.hp > 0
    
    def get_total_attack(self) -> int:
        """Get total attack including equipment and status effect bonuses."""
        total = self.attack
        # Equipment bonuses
        for item in self.equipped.values():
            total += item.stats.get("attack", 0)
        # Status effect bonuses
        for effect in self.status_effects:
            total += effect.get_stat_modifier("attack")
        return max(0, total)
    
    def get_total_defense(self) -> int:
        """Get total defense including equipment and status effect bonuses."""
        total = self.defense
        # Equipment bonuses
        for item in self.equipped.values():
            total += item.stats.get("defense", 0)
        # Status effect bonuses
        for effect in self.status_effects:
            total += effect.get_stat_modifier("defense")
        return max(0, total)
    
    def add_status_effect(self, status_effect: StatusEffect):
        """Add a status effect to the character."""
        # Check if the same effect type already exists
        for existing_effect in self.status_effects:
            if existing_effect.effect_type == status_effect.effect_type:
                # Replace with new effect (refresh duration)
                self.status_effects.remove(existing_effect)
                break
        
        self.status_effects.append(status_effect)
    
    def remove_status_effect(self, effect_type: StatusEffectType):
        """Remove a specific type of status effect."""
        self.status_effects = [effect for effect in self.status_effects 
                              if effect.effect_type != effect_type]
    
    def has_status_effect(self, effect_type: StatusEffectType) -> bool:
        """Check if character has a specific status effect."""
        return any(effect.effect_type == effect_type for effect in self.status_effects)
    
    def is_action_prevented(self) -> bool:
        """Check if character is prevented from acting due to status effects."""
        return any(effect.prevents_action() for effect in self.status_effects)
    
    def process_status_effects(self) -> List[str]:
        """Process all status effects and return messages."""
        messages = []
        expired_effects = []
        
        for effect in self.status_effects:
            message = effect.apply_effect(self)
            if message:
                messages.append(message)
            
            if effect.is_expired():
                expired_effects.append(effect)
        
        # Remove expired effects
        for effect in expired_effects:
            self.status_effects.remove(effect)
            messages.append(f"{self.name}'s {effect.name} has worn off.")
        
        return messages
    
    def get_status_effects_summary(self) -> List[str]:
        """Get a summary of active status effects."""
        return [str(effect) for effect in self.status_effects]
    
    def update_cooldowns(self):
        """Update all ability cooldowns."""
        for ability in self.abilities:
            ability.reduce_cooldown()


class Player(Character):
    """Player character with leveling system."""
    
    def __init__(self, name: str, hp: int = 100, mana: int = 50, 
                 attack: int = 10, defense: int = 5):
        super().__init__(name, hp, mana, attack, defense)
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        self.gold = 0
        self.stat_points = 0
    
    def gain_experience(self, exp: int):
        """Gain experience points and level up if necessary."""
        self.experience += exp
        
        while self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Level up the player."""
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.experience_to_next_level = int(self.experience_to_next_level * 1.2)
        
        # Increase stats on level up
        hp_increase = random.randint(8, 12)
        mana_increase = random.randint(3, 7)
        attack_increase = random.randint(1, 3)
        defense_increase = random.randint(1, 2)
        
        self.max_hp += hp_increase
        self.hp += hp_increase
        self.max_mana += mana_increase
        self.mana += mana_increase
        self.attack += attack_increase
        self.defense += defense_increase
        self.stat_points += 2
        
        return f"{self.name} leveled up to level {self.level}!"
    
    def allocate_stat_point(self, stat: str):
        """Allocate a stat point to a specific stat."""
        if self.stat_points > 0 and hasattr(self, stat):
            if stat in ["max_hp", "max_mana", "attack", "defense"]:
                setattr(self, stat, getattr(self, stat) + 1)
                if stat == "max_hp":
                    self.hp += 1
                elif stat == "max_mana":
                    self.mana += 1
                self.stat_points -= 1
                return True
        return False
    
    def add_gold(self, amount: int):
        """Add gold to player."""
        self.gold += amount
    
    def spend_gold(self, amount: int) -> bool:
        """Spend gold if player has enough."""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False


class Enemy(Character):
    """Enemy character with customizable attributes and drop system."""
    
    def __init__(self, name: str, hp: int = 50, mana: int = 20, 
                 attack: int = 8, defense: int = 3, level: int = 1,
                 exp_reward: int = 25, gold_reward: int = 10):
        super().__init__(name, hp, mana, attack, defense)
        self.level = level
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.drop_table: List[Dict[str, Any]] = []  # List of {item: Item, chance: float}
    
    def add_drop(self, item: Item, chance: float):
        """Add an item to the enemy's drop table."""
        self.drop_table.append({"item": item, "chance": chance})
    
    def get_drops(self) -> List[Item]:
        """Get random drops based on drop table."""
        drops = []
        for drop_data in self.drop_table:
            if random.random() < drop_data["chance"]:
                drops.append(drop_data["item"])
        return drops
    
    def ai_choose_ability(self, target: Character) -> Optional[Ability]:
        """Enhanced AI to choose an ability with status effect prioritization."""
        usable_abilities = [ability for ability in self.abilities if ability.can_use(self)]
        
        if not usable_abilities:
            return None
        
        # Priority 1: Heal if critically low HP
        if self.hp < self.max_hp * 0.25:
            heal_abilities = [a for a in usable_abilities if a.ability_type == AbilityType.HEAL]
            if heal_abilities:
                return random.choice(heal_abilities)
        
        # Priority 2: Use self-buffs if not already buffed
        if not any(effect.effect_type in [StatusEffectType.STRENGTH_BOOST, StatusEffectType.DEFENSE_BOOST, 
                                         StatusEffectType.SPEED_BOOST, StatusEffectType.REGENERATION] 
                  for effect in self.status_effects):
            buff_abilities = [a for a in usable_abilities if a.ability_type == AbilityType.BUFF]
            if buff_abilities:
                return random.choice(buff_abilities)
        
        # Priority 3: Apply debuffs if target doesn't have them
        if not target.has_status_effect(StatusEffectType.POISON) and not target.has_status_effect(StatusEffectType.BURN):
            damage_over_time_abilities = [a for a in usable_abilities 
                                        if hasattr(a, 'status_effect') and a.status_effect 
                                        and a.status_effect.effect_type in [StatusEffectType.POISON, StatusEffectType.BURN]]
            if damage_over_time_abilities:
                return random.choice(damage_over_time_abilities)
        
        # Priority 4: Apply crowd control if target isn't already controlled
        if not target.has_status_effect(StatusEffectType.STUN) and not target.has_status_effect(StatusEffectType.FREEZE):
            cc_abilities = [a for a in usable_abilities 
                          if hasattr(a, 'status_effect') and a.status_effect 
                          and a.status_effect.effect_type in [StatusEffectType.STUN, StatusEffectType.FREEZE]]
            if cc_abilities:
                return random.choice(cc_abilities)
        
        # Priority 5: Apply stat debuffs if target doesn't have them
        if not target.has_status_effect(StatusEffectType.WEAKNESS) and not target.has_status_effect(StatusEffectType.VULNERABILITY):
            debuff_abilities = [a for a in usable_abilities 
                              if hasattr(a, 'status_effect') and a.status_effect 
                              and a.status_effect.effect_type in [StatusEffectType.WEAKNESS, StatusEffectType.VULNERABILITY]]
            if debuff_abilities:
                return random.choice(debuff_abilities)
        
        # Priority 6: Use high-damage attacks
        high_damage_abilities = [a for a in usable_abilities 
                               if a.ability_type == AbilityType.ATTACK and a.power >= 20]
        if high_damage_abilities:
            return random.choice(high_damage_abilities)
        
        # Priority 7: Use any attack ability
        attack_abilities = [a for a in usable_abilities if a.ability_type == AbilityType.ATTACK]
        if attack_abilities:
            return random.choice(attack_abilities)
        
        # Fallback: Use any available ability
        return random.choice(usable_abilities)


class Shop:
    """Shop system for buying and selling items."""
    
    def __init__(self, name: str = "General Store"):
        self.name = name
        self.inventory: List[Item] = []
        self.buy_price_multiplier = 1.0
        self.sell_price_multiplier = 0.5
    
    def add_item(self, item: Item, quantity: int = 1):
        """Add items to shop inventory."""
        for _ in range(quantity):
            self.inventory.append(item)
    
    def remove_item(self, item: Item) -> bool:
        """Remove an item from shop inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def get_buy_price(self, item: Item) -> int:
        """Get the price to buy an item."""
        return int(item.value * self.buy_price_multiplier)
    
    def get_sell_price(self, item: Item) -> int:
        """Get the price to sell an item."""
        return int(item.value * self.sell_price_multiplier)
    
    def buy_item(self, player: Player, item: Item) -> bool:
        """Player buys an item from the shop."""
        if item not in self.inventory:
            return False
        
        price = self.get_buy_price(item)
        if player.spend_gold(price):
            self.remove_item(item)
            player.add_item(item)
            return True
        return False
    
    def sell_item(self, player: Player, item: Item) -> bool:
        """Player sells an item to the shop."""
        if item not in player.inventory:
            return False
        
        price = self.get_sell_price(item)
        player.inventory.remove(item)
        player.add_gold(price)
        self.add_item(item)
        return True
    
    def list_items(self) -> List[str]:
        """Get a list of items in the shop with prices."""
        items = {}
        for item in self.inventory:
            if item.name in items:
                items[item.name]["quantity"] += 1
            else:
                items[item.name] = {
                    "item": item,
                    "quantity": 1,
                    "price": self.get_buy_price(item)
                }
        
        return [f"{data['item'].name} x{data['quantity']} - {data['price']} gold" 
                for data in items.values()]