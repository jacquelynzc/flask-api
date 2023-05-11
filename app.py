from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('fruits', 
                        user='rude', 
                        password='', 
                        port='5432')

class BaseModel(Model): 
    class Meta:
        database = db
        
class Fruit(BaseModel):
    name = CharField()
    color = CharField()
    shape = CharField()
    
db.connect()
# db.drop_tables([Fruit])
# db.create_tables([Fruit])

# Fruit(name='Strawberry', color='red', shape='triangular').save()
# Fruit(name='Blueberry', color='blue', shape='spherical').save()
# Fruit(name='Green Grape', color='green', shape='spherical').save()
# Fruit(name='Red Grape', color='purple', shape='spherical').save()
# Fruit(name='Avocado', color='green', shape='oblong').save()

app = Flask(__name__)

@app.route('/fruits/', methods=['GET', 'POST'])
@app.route('/fruits/<id>', methods=['GET', 'PUT', 'DELETE'])

def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Fruit.get(Fruit.id == id)))
        else:
            fruit_list = []
            for fruit in Fruit.select():
                fruit_list.append(model_to_dict(fruit))
            return jsonify(fruit_list)
        
    if request.method == "POST":
        new_fruit = dict_to_model(Fruit, request.get_json())
        new_fruit.save()
        return jsonify({'success': True})
    
    if request.method == "PUT":
        body = request.get_json()
        Fruit.update(body).where(Fruit.id == id).execute()
        return f'Fruit {id} has been updated'
    
    if request.method == "DELETE":
        Fruit.delete().where(Fruit.id == id).execute()
        return f'Fruit {id} has been deleted'
        
@app.route("/")
def index():
    return 'I love fruits!'

app.run(port=9000, debug=True)