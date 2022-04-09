import pytest

from animal import Animal
from zoo import Zoo
from care_taker import CareTaker

@pytest.fixture
def tiger1 ():
    return Animal ("tiger", "ti", 12)

@pytest.fixture
def tiger2 ():
    return Animal ("tiger2", "ti", 2)

@pytest.fixture
def zoo1 ():
    return Zoo ()

@pytest.fixture
def caretaker1():
    return CareTaker("Joe", "SunnyStreet 18, Austria")


def test_addAnimal(zoo1, tiger1, tiger2, caretaker1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addEmployee(caretaker1)
    assert (caretaker1 in zoo1.employees)
    caretaker1.addAnimal(tiger1)
    caretaker1.addAnimal(tiger2)

    assert (len(caretaker1.list_of_animals) == 2)

def test_removeAnimal(zoo1, tiger1, tiger2, caretaker1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addEmployee(caretaker1)

    caretaker1.addAnimal(tiger1)
    caretaker1.addAnimal(tiger2)

    assert (len(caretaker1.list_of_animals) == 2)

    caretaker1.removeAnimal(tiger2)

    assert (len(caretaker1.list_of_animals) == 1)
    assert (tiger2 not in caretaker1.list_of_animals)