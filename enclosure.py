import uuid
import datetime


class Enclosure:
    def __init__(self, name, area):
        self.enclosure_id = str(uuid.uuid4())
        self.name = name
        self.available_space = area
        self.animals = []
        self.cleaning_record = []

    def addAnimal(self, animal):
        self.animals.append(animal)

    def removeAnimal(self, animal):
        self.animals.remove(animal)

    def clean(self):
        self.cleaning_record.append(datetime.datetime.now())

    def getAnimals(self):
        pass

