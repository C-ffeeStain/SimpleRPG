from enum import Enum
from pydantic import BaseModel, validator


class Direction(Enum):
    """
    Enum class for directions.
    """

    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class EntityStats:
    def __init__(self, defense: int, attack: int, max_hp: int):
        self.defense = defense
        self.attack = attack
        self.max_hp = max_hp
        self.hp = max_hp


class Item:
    def __init__(self, name: str, description: str, type: str):
        self.name = name
        self.description = description


class Weapon(Item):
    def __init__(self, name: str, description: str, damage: int):
        super().__init__(name, description)
        self.damage = damage


class Armor(Item):
    def __init__(self, name: str, description: str, defense: int):
        super().__init__(name, description)
        self.defense = defense


class Entity:
    def __init__(self, name: str, stats: EntityStats, alive: bool = True):
        self.name = name
        self.stats = stats
        self.alive = alive

    def damage(self, damage: int, attacker: str = None):
        self.stats.hp -= damage
        if self.stats.hp <= 0:
            self.stats.hp = 0
            self.alive = False


class Inventory:
    items: "list[Item]" = []
    max_items: int = 10
    armor: dict = {
        "head": None,
        "chest": None,
        "legs": None,
        "feet": None,
        "shield": None,
    }
    mainhand: "Weapon" = None

    def __init__(self):
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.max_items:
            self.items.append(item)
        else:
            print("Your inventory is full!")

    def remove_item(self, item):
        self.items.remove(item)


class Player(Entity):
    """
    Player class.
    """

    def __init__(self, name: str, stats: EntityStats):
        super().__init__(name, stats)
        self.inventory = Inventory()

    def damage(self, damage: int, attacker: str = None):
        for item in self.inventory.items:
            if item.type == "Shield":
                damage -= item.stats.defense


class Monster(Entity):
    """
    Monster class.
    """

    def __init__(self, name: str, stats: EntityStats):
        super().__init__(name, stats.max_hp, stats)
        self.current_health = self.stats.max_hp
