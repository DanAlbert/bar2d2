"""Logic for creating new drinks.

Author: Dan Albert <dan@gingerhq.net>
"""
from models import Drink, Ingredient


def random_name():
    pass


def random_drink():
    ingredients = random_ingredients(3)
    name = random_name()
    return Drink(name=name, ingredients=ingredients)


def random_ingredients(num):
    keys = Ingredient.all(keys_only=True)
    keys = random.sample(keys.fetch(), num)
    return Ingredient.get(keys)
