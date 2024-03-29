from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'ricardo'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="esta campo no puede venir en blanco"
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message' : "Un item con el nombre '{}' ya existe.".format(name)}, 400
        
        data = Item.parser.parse_args() # refactorizada la forma de leer los datos del request (Item es el nombre de la clase)

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item eliminado'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price'] }
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(delf):
        return {'items': items}       

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/silla
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items

app.run(port=5000, debug=True)