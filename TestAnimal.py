import pytest

from animal import Animal
from zoo import Zoo
from enclosure import Enclosure
from care_taker import CareTaker


# Animals
@pytest.fixture
def tiger1():
    return Animal("tiger", "ti", 12)


@pytest.fixture
def tiger2():
    return Animal("tiger2", "ti", 2)


# Zoo
@pytest.fixture
def zoo1():
    return Zoo()


# Enclosure
@pytest.fixture
def enclosure1():
    return Enclosure("tiger cage", 5)


# Caretaker
@pytest.fixture
def caretaker1():
    return CareTaker("Joe", "SunnyStreet 18, Austria")


def test_addingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    # Is the animal in the list
    assert (tiger1 in zoo1.animals)
    zoo1.addAnimal(tiger2)

    # Checks the length of the list of animals
    assert (len(zoo1.animals) == 2)


def test_feedingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)

    tiger1.feed()
    # Checks the length of animal's feeding record
    assert (len(tiger1.feeding_record) == 1)


def test_vetAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)

    tiger1.vet()
    # Checks the length of animal's vet record
    assert (len(tiger1.vet_record) == 1)


def test_setEnclosure(zoo1, tiger1, enclosure1):
    zoo1.addAnimal(tiger1)

    tiger1.setEnclosure(enclosure1.enclosure_id)
    # Compares animal's enclosure id and enclosure's id
    assert (tiger1.enclosure == enclosure1.enclosure_id)


def test_birthAnimal(zoo1, tiger1, enclosure1):
    zoo1.addAnimal(tiger1)
    zoo1.addEnclosure(enclosure1)
    tiger1.setEnclosure(enclosure1.enclosure_id)

    small_tiger = tiger1.birth()
    # Compares animal's enclosure id and animal child's enclosure id
    assert (tiger1.enclosure == small_tiger.enclosure)
    # Checks the animal child's age
    assert (small_tiger.age == 0)
    # Compares animal's and animal child's common name
    assert (small_tiger.common_name == tiger1.common_name)
    # Compares animal's and animal child's species name
    assert (small_tiger.species_name == tiger1.species_name)


def test_caretakerAnimal(zoo1, tiger1, caretaker1):
    zoo1.addAnimal(tiger1)
    zoo1.addEmployee(caretaker1)
    tiger1.assign_caretaker(caretaker1.employee_id)
    # Compares animal's caretaker id and caretaker's id
    assert (tiger1.care_taker == caretaker1.employee_id)
