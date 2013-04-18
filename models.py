"""Models used by the application.

Author: Dan Albert <dan@gingerhq.net>
"""
import db
import json

class DictProperty(db.Property):
    data_type = type('')

    def get_value_for_datastore(self, model_instance):
        data = super(DictProperty, self).get_value_for_datastore(model_instance)
        return json.loads(data)

    def get_value_from_datastore(self, value):
        if value is None:
            return None

        return json.dumps(value)


class Ingredient(db.Model):
    """A D20 character."""
    name = db.StringProperty()
    price = db.FloatProperty("Price per unit volume (USD/liter)")
    abv = db.IntegerProperty("Alcohol content by volume as a percentage")

    @property
    def proof(self):
        return self.abv * 2

    def __unicode__(self):
        return self.name


class Drink(db.Model):
    name = db.StringProperty()
    ingredients = DictProperty()

    @property
    def price(self):
        raise NotImplementedError()

    @property
    def abv(self):
        raise NotImplementedError()

    @property
    def volume(self):
        raise NotImplementedError()

    def __unicode__(self):
        return name
