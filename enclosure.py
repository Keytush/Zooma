import uuid
import datetime


class Enclosure:
    def __init__(self, name, area):
        self.enclosure_id = str(uuid.uuid4())
        self.name = name
        self.available_space = area
        self.animals = []
        self.cleaning_record = []

    # Add animal to enclosure's list of animals
    def addAnimal(self, animal):
        self.animals.append(animal)

    # Remove animal from enclosure's list of animals
    def removeAnimal(self, animal):
        self.animals.remove(animal)

    # Register a time of cleaning
    def clean(self):
        self.cleaning_record.append(datetime.datetime.now())