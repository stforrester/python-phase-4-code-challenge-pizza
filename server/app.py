#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=['GET'])
def restaurants():
    restaurants = [restaurant.to_dict(rules=("-restaurant_pizzas",)) for restaurant in Restaurant.query.all()]
    
    if request.method == 'GET':
        response = make_response(
            restaurants,
            200
        )

        return response

@app.route("/restaurants/<int:id>", methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()

    if request.method == 'GET':
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            response = make_response(
                restaurant_dict,
                200
            )

        else:
            response = make_response(
                {"error":"Restaurant not found"},
                404
            )
        
        return response
    
    elif request.method == 'DELETE':
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Restaurant deleted."
            }

            response = make_response(
                response_body,
                200
            )
        else:
            response = make_response(
                {"error":"Restaurant not found"},
                404
            )
        
        return response

@app.route("/pizzas", methods=['GET'])
def pizzas():
    pizzas = [pizza.to_dict(rules=("-restaurant_pizzas",)) for pizza in Pizza.query.all()]

    if request.method == 'GET':
        response = make_response(
            pizzas,
            200
        )

        return response

@app.route("/restaurant_pizzas", methods=['GET', 'POST'])
def restaurant_pizzas():
    restaurant_pizzas = [restaurant_pizza.to_dict() for restaurant_pizza in RestaurantPizza.query.all()]

    if request.method == 'GET':
        response = make_response(
            restaurant_pizzas,
            200
        )

        return response
    
    

if __name__ == "__main__":
    app.run(port=5555, debug=True)
