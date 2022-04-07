from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder
from zoo import Zoo

from animal import Animal
from enclosure import Enclosure
from care_taker import CareTaker


my_zoo = Zoo()

zooma_app = Flask(__name__)
# need to extend this class for custom objects, so that they can be jsonified
zooma_app.json_encoder = ZooJsonEncoder
zooma_api = Api(zooma_app)

# creating a parser for animal
animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True,
                           help='The scientific name of the animal, e.g., Panthera tigris')
animal_parser.add_argument('name', type=str, required=True, help='The common name of the animal, e.g., Tiger')
animal_parser.add_argument('age', type=int, required=True, help='The age of the animal, e.g., 12')

# creating a parser for enclosure
enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('name', type=str, required=True, help="The name of the animal's enclosure, e.g., tiger "
                                                                    "cave 213")
enclosure_parser.add_argument('area', type=float, required=True, help="The available space of the animal's enclosure "
                                                                      "in meters, e.g., 5.0")
# creating a parser for animal's home (enclosure)
home_parser = reqparse.RequestParser()
home_parser.add_argument('enclosure_id', type=str, required=True)

# creating a parser for an animal birth
birth_parser = reqparse.RequestParser()
birth_parser.add_argument('mother_id', type=str, required=True)

# creating a parser for an animal death
death_parser = reqparse.RequestParser()
death_parser.add_argument('animal_id', type=str, required=True)

# creating a parser for employee
employee_parser = reqparse.RequestParser()
employee_parser.add_argument('name', type=str, required=True, help='The name of a caretaker, e.g., John Smith')
employee_parser.add_argument('address', type=str, required=True, help="The address of a caretaker, e.g., Sunnystreet "
                                                                      "9, 2410 Austria")



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
        return jsonify(search_result)  # this is automatically jsonified by flask-restx

    def delete(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        # If the animal does not exist, return a message
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        # If the animal has an enclosure
        # Remove the animal from enclosure
        enclosure = my_zoo.getEnclosure(targeted_animal.enclosure)
        if enclosure:
            enclosure.removeAnimal(targeted_animal)
        # Remove animal from zoo
        my_zoo.removeAnimal(targeted_animal)
        return jsonify(f"Animal with ID {animal_id} was removed")


@zooma_api.route('/animals')
class AllAnimals(Resource):
    def get(self):
        return jsonify(my_zoo.animals)


@zooma_api.route('/animal/<animal_id>/feed')
class FeedAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.feed()
        return jsonify(targeted_animal)


@zooma_api.route('/animal/<animal_id>/vet')
class VetAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        targeted_animal.vet()
        return jsonify(targeted_animal)


@zooma_api.route('/animal/<animal_id>/home')
class HomeAnimal(Resource):
    @zooma_api.doc(parser=home_parser)
    def post(self, animal_id):
        # get the targeted animal
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")

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
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")

        # add the animal in the enclosure list
        targeted_enclosure.addAnimal(targeted_animal)
        # sets the enclosure to the animal
        targeted_animal.setEnclosure(enclosure_id)
        return jsonify(targeted_animal)


@zooma_api.route('/animal/birth')
class BornAnimal(Resource):
    @zooma_api.doc(parser=birth_parser)
    def post(self):
        args = birth_parser.parse_args()
        mother_id = args['mother_id']
        targeted_animal = my_zoo.getAnimal(mother_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {mother_id} was not found")
        enclosure = my_zoo.getEnclosure(targeted_animal.enclosure)
        child = targeted_animal.birth(my_zoo)
        my_zoo.addAnimal(child)
        if enclosure:
            enclosure.addAnimal(child)

        return jsonify(child)


@zooma_api.route('/animal/death')
class DeathAnimal(Resource):
    @zooma_api.doc(parser=death_parser)
    def post(self):
        args = death_parser.parse_args()
        animal_id = args['animal_id']
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        enclosure = my_zoo.getEnclosure(targeted_animal.enclosure)
        my_zoo.removeAnimal(targeted_animal)
        if enclosure:
            enclosure.removeAnimal(targeted_animal)

        return jsonify(f"Animal with ID {animal_id} was removed")


@zooma_api.route('/animals/stat')
class AnimalsStat(Resource):
    def get(self):
        return jsonify(my_zoo.getAnimalStat())


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


@zooma_api.route('/enclosures/<enclosure_id>/clean')
class CleanEnclosure(Resource):
    def post(self, enclosure_id):
        targeted_enclosure = my_zoo.getEnclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        targeted_enclosure.clean()
        return jsonify(targeted_enclosure)


@zooma_api.route('/enclosures/<enclosure_id>/animals')
class AnimalsInEnclosure(Resource):
    def get(self, enclosure_id):
        targeted_enclosure = my_zoo.getEnclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        animals = targeted_enclosure.animals
        return jsonify(animals)


@zooma_api.route('/enclosure/<enclosure_id>')
class RemoveEnclosure(Resource):
    def delete(self, enclosure_id):
        targeted_enclosure = my_zoo.getEnclosure(enclosure_id)
        # If the enclosure does not exist, return a message
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        if not my_zoo.animals:
            my_zoo.removeEnclosure(targeted_enclosure)
            return jsonify(f"Enclosure with ID {enclosure_id} was removed")
        if len(my_zoo.enclosures) <= 1:
            return jsonify("Cannot remove enclosure and transfer its animals, due to lack of enclosures")
        # If the animal has an enclosure
        # Remove the animal from enclosure
        animals = targeted_enclosure.animals
        if animals:
            # move them into other enclosure
            pass
        # Remove enclosure from zoo
        my_zoo.removeEnclosure(targeted_enclosure)
        return jsonify(f"Enclosure with ID {enclosure_id} was removed")


@zooma_api.route('/employee')
class AddEmployeeAPI(Resource):
    @zooma_api.doc(parser=employee_parser)
    def post(self):
        # get the post parameters
        args = employee_parser.parse_args()
        name = args['name']
        address = args['address']
        new_employee = CareTaker(name, address)
        my_zoo.addEmployee(new_employee)
        return jsonify(new_employee)


@zooma_api.route('/employee/<employee_id>/care/<animal_id>')
class AssignAnimalToCaretaker(Resource):
    def post(self, employee_id, animal_id):
        # Get employee
        targeted_employee = my_zoo.getEmployee(employee_id)
        if not targeted_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")
        # Get animal
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify(f"Animal with ID {animal_id} was not found")
        # Get animal's caretaker
        old_caretaker = my_zoo.getEmployee(targeted_animal.care_taker)
        # If animal has caretaker, remove the animal from him
        if old_caretaker:
            old_caretaker.remove_animal(targeted_animal)
        # Assign caretaker to animal
        targeted_animal.assign_caretaker(employee_id)
        # Assign animal to caretaker
        targeted_employee.addAnimal(targeted_animal)
        return jsonify(targeted_animal)


@zooma_api.route('/employee/<employee_id>/care/animals')
class GetCaretakerAnimals(Resource):
    def get(self, employee_id):
        # Get employee
        targeted_employee = my_zoo.getEmployee(employee_id)
        if not targeted_employee:
            return jsonify(f"Employee with ID {employee_id} was not found")
        return jsonify(targeted_employee.list_of_animals)




if __name__ == '__main__':
    zooma_app.run(debug=False, port=7890)
