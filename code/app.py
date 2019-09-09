from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = 'ricardo'
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message' : "Un item con el nombre '{}' ya existe.".format(name)}, 400
        
        data = request.get_json(force = True) # silent=Tue
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(delf):
        return {'items': items}       

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/silla
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items

app.run(port=5000, debug=True)