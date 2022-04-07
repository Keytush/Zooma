import uuid
import datetime


class Animal:
    def __init__(self, species_name, common_name, age):
        self.animal_id = str(uuid.uuid4())
        self.species_name = species_name
        self.common_name = common_name
        self.age = age
        self.feeding_record = []
        self.enclosure = None
        self.care_taker = None
        # add more as required here
        self.vet_record = []

    # simply store the current system time when this method is called
    def feed(self):
        self.feeding_record.append(datetime.datetime.now())

    def vet(self):
        self.vet_record.append(datetime.datetime.now())

    def setEnclosure(self, enclosure_id):
        self.enclosure = enclosure_id

    def birth(self):
        child = Animal(self.species_name, self.common_name, 0)
        # zoo.addAnimal(child)
        child.enclosure = self.enclosure
        # if self.enclosure:
        #     enclosure1 = zoo.getEnclosure(self.enclosure)
        #     enclosure1.animals.append(child)
        return child

    def assign_caretaker(self, care_taker_id):
        self.care_taker = care_taker_id


