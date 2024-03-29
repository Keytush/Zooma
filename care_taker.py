import uuid


class CareTaker:
    def __init__(self, name, address):
        self.employee_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.list_of_animals = []
        self.feeding_plan = {}  # every 2nd day
        self.enclosure_cleaning_plan = {}   # every 3rd day
        self.medical_check_up_plan = {}     # every 5 weeks

    # Add animal to caretaker's list of animals
    def addAnimal(self, animal):
        self.list_of_animals.append(animal)

    # Remove animal from caretaker's list of animals
    def removeAnimal(self, animal):
        self.list_of_animals.remove(animal)