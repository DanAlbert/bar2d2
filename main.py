"""Entry point for D20 Character Manager.

Author: Dan Albert <dan@gingerhq.net>
"""
import webapp2
from webapp2 import uri_for

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2

import json
import logging
import os
import urllib2

import auth
import settings

from models import Ingredient

jinja = jinja2.Environment(
            loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIR))


def format_currency(value):
    return "${:,.2f}".format(value)


jinja.filters['currency'] = format_currency


class RequestHandler(webapp2.RequestHandler):
    """Base request handler that handles site wide handling tasks."""
    def render(self, template_name, data={}):
        """Renders the template in the site wide manner.
        
        Retrieves the template data needed for the base template (login URL and
        text, user information, etc.) and merges it with the data passed to the
        method. Templates are retrieved from the template directory specified in
        the settings and appended with the suffix ".html"
        
        Arguments:
        template_name: the name of the template. this is the file name of the
                       template without the .html extension.

        data: a dictionary containing data to be passed to the template.
        """
        (login_text, login_url) = auth.login_logout(self.request)
        
        data['uri_for'] = webapp2.uri_for

        data['user'] = auth.current_user()
        data['admin'] = auth.user_is_admin()
        data['login_url'] = login_url
        data['login_text'] = login_text
        
        template = jinja.get_template(template_name + '.html')
        return self.response.out.write(template.render(data))


class IngredientListHandler(RequestHandler):
    def get(self):
        return self.render('ingredient-list')


class JsonIngredientListHandler(RequestHandler):
    def get(self):
        ingredients = []
        for ingredient in Ingredient.all().order('name'):
            ingredients.append({
                'name': ingredient.name,
                'price': ingredient.price,
                'abv': ingredient.abv,
            })
        self.response.out.write(json.dumps(ingredients))

    def post(self):
        form = json.loads(self.request.get('form'))
        name = form['name']
        price = float(form['price']) * (4.0 / 3.0)  # 750ml to 1L
        abv = int(form['abv'])
        ingredient = Ingredient(name=name, price=price, abv=abv)
        ingredient.put()


class IngredientHandler(RequestHandler):
    def get(self, key):
        ingredient = Ingredient.get(key)
        return self.render('ingredient', {'ingrdient': ingredient})

    def put(self, key):
        ingredient = Ingredient.get(key)
        form = json.loads(self.request.get('form'))
        ingredient.name = form['name']
        ingredient.price = float(form['price'])
        ingredient.abv = int(form['abv'])
        ingredient.put()

    def delete(self, key):
        Ingredient.get(key).delete()


app = webapp2.WSGIApplication([
    ('/', IngredientListHandler),
    webapp2.Route(r'/ingredient', name='ingredient-list',
                  handler=IngredientListHandler, methods=['GET', 'POST']),
    webapp2.Route(r'/ingredient/<key>', name='ingredient',
                  handler=IngredientHandler, methods=['GET', 'PUT', 'DELETE']),
    webapp2.Route(r'/json/ingredient', name='json-ingredient-list',
                  handler=JsonIngredientListHandler, methods=['GET', 'POST']),
], debug=True)
