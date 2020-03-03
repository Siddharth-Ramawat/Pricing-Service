# from flask import Blueprint
#
# learning_blueprint = Blueprint('learning', __name__)
#
#
# @learning_blueprint.route('/')
# def home():
# 	return "Hello World"
from models.item import Item

item = Item.get_by_id("7ecea1fe66a44083b00917e7bdbc3666")
print(item.load_price())

