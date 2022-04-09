import pytest

from animal import Animal
from zoo import Zoo
from enclosure import Enclosure
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
def enclosure1():
    return Enclosure("tiger cage", 5)

@pytest.fixture
def caretaker1():
    return CareTaker("Joe", "SunnyStreet 18, Austria")

def test_addingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    assert (tiger1 in zoo1.animals)
    zoo1.addAnimal(tiger2)

    assert (len(zoo1.animals)==2)

def test_feedingAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)

    tiger1.feed()

    assert (len(tiger1.feeding_record)==1)

def test_vetAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)

    tiger1.vet()

    assert (len(tiger1.vet_record)==1)

def test_setEnclosure(zoo1, tiger1, enclosure1):
    zoo1.addAnimal(tiger1)

    tiger1.setEnclosure(enclosure1.enclosure_id)

    assert (tiger1.enclosure == enclosure1.enclosure_id)

def test_birthAnimal(zoo1, tiger1, enclosure1):
    zoo1.addAnimal(tiger1)
    zoo1.addEnclosure(enclosure1)
    tiger1.setEnclosure(enclosure1.enclosure_id)

    small_tiger = tiger1.birth()

    assert (tiger1.enclosure == small_tiger.enclosure)
    assert (small_tiger.age == 0)
    assert (small_tiger.common_name == tiger1.common_name)
    assert (small_tiger.species_name == tiger1.species_name)

def test_caretakerAnimal(zoo1, tiger1, caretaker1):
    zoo1.addAnimal(tiger1)
    zoo1.addEmployee(caretaker1)
    tiger1.assign_caretaker(caretaker1.employee_id)

    assert (tiger1.care_taker == caretaker1.employee_id)


