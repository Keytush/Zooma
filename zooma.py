from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder
from zoo import Zoo

from animal import Animal
from enclosure import Enclosure

my_zoo = Zoo()

zooma_app = Flask(__name__)
# need to extend this class for custom objects, so that they can be jsonified
zooma_app.json_encoder = ZooJsonEncoder
zooma_api = Api(zooma_app)

animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True,
                           help='The scientific name of the animal, e.g., Panthera tigris')
animal_parser.add_argument('name', type=str, required=True, help='The common name of the animal, e.g., Tiger')
animal_parser.add_argument('age', type=int, required=True, help='The age of the animal, e.g., 12')

enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('name', type=str, required=True, help="The name of the animal's enclosure, e.g., tiger "
                                                                    "cave 213")
enclosure_parser.add_argument('area', type=float, required=True, help="The available space of the animal's enclosure "
                                                                      "in meters, e.g., 5.0")

home_parser = reqparse.RequestParser()
home_parser.add_argument('enclosure_id', type=str, required=True)


@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters 
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        # create a new animal object 
        new_animal = Animal(species, name, age)
        # add the animal to the zoo
        my_zoo.addAnimal(new_animal)
        return jsonify(new_animal)


@zooma_api.route('/animal/<animal_id>')
class Animal_ID(Resource):
    def get(self, animal_id):
        search_result = my_zoo.getAnimal(animal_id)
        return search_result  # this is automatically jsonified by flask-restx

    def delete(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")
        my_zoo.removeAnimal(targeted_animal)
        return jsonify("Animal with ID {animal_id} was removed")


@zooma_api.route('/animals')
class AllAnimals(Resource):
    def get(self):
        return jsonify(my_zoo.animals)


@zooma_api.route('/animals/<animal_id>/feed')
class FeedAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")
        targeted_animal.feed()
        return jsonify(targeted_animal)


@zooma_api.route('/animals/<animal_id>/vet')
class VetAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")
        targeted_animal.vet()
        return jsonify(targeted_animal)


@zooma_api.route('/animal/<animal_id>/home')
class HomeAnimal(Resource):
    @zooma_api.doc(parser=home_parser)
    def post(self, animal_id):
        # get the targeted animal
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")

        # get the old enclosure from an animal
        old_enclosure = my_zoo.getEnclosure(targeted_animal.enclosure)

        if old_enclosure:
            old_enclosure.removeAnimal(targeted_animal)


        # input
        args = home_parser.parse_args()
        enclosure_id = args['enclosure_id']
        # get the enclosure
        targeted_enclosure = my_zoo.getEnclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify("Enclosure with ID {enclosure_id} was not found")

        # add the animal in the enclosure list
        targeted_enclosure.addAnimal(targeted_animal)
        # sets the enclosure to the animal
        targeted_animal.setEnclosure(enclosure_id)
        return jsonify(targeted_animal)


@zooma_api.route('/enclosure')
class AddEnclosureAPI(Resource):
    @zooma_api.doc(parser=enclosure_parser)
    def post(self):
        # get the post parameters
        args = enclosure_parser.parse_args()
        name = args['name']
        area = args['area']
        new_enclosure = Enclosure(name, area)
        my_zoo.addEnclosure(new_enclosure)
        return jsonify(new_enclosure)


@zooma_api.route('/enclosures')
class AllEnclosures(Resource):
    def get(self):
        return jsonify(my_zoo.enclosures)


if __name__ == '__main__':
    zooma_app.run(debug=False, port=7890)
