import pytest
import datetime

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


@pytest.fixture
def tiger3():
    return Animal("tiger2", "ti", 2)


# Zoo
@pytest.fixture
def zoo1():
    return Zoo()


# Enclosures
@pytest.fixture
def enclosure1():
    return Enclosure("tiger cage", 5)


@pytest.fixture
def enclosure2():
    return Enclosure("lion cage", 10)


# Employees
@pytest.fixture
def caretaker1():
    return CareTaker("Joe", "SunnyStreet 18, Austria")


@pytest.fixture
def caretaker2():
    return CareTaker("Senna", "FunnyStreet 15, France")


def test_addAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    # Is the animal in the list
    assert (tiger1 in zoo1.animals)
    # Checks the length of the list of animals
    assert (len(zoo1.animals) == 1)


def test_removeAnimal(zoo1, tiger1, tiger2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)

    zoo1.removeAnimal(tiger2)
    # Checks the length of the list of animals
    assert (len(zoo1.animals) == 1)
    # Is the removed animal not in the list
    assert (tiger2 not in zoo1.animals)
    # Is the animal in the list
    assert (tiger1 in zoo1.animals)


def test_getAnimal(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    animal = zoo1.getAnimal(tiger1.animal_id)
    assert (animal == tiger1)


def test_getAnimalSpecies(zoo1, tiger1, tiger2, tiger3):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)

    animalSpecies = zoo1.getAnimalSpecies()

    expected = {
        'tiger': 1,
        'tiger2': 2
    }

    assert (animalSpecies == expected)


def test_getAnimalStat(zoo1, tiger1, tiger2, tiger3, enclosure1, enclosure2):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)

    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)

    enclosure1.addAnimal(tiger1)
    enclosure1.addAnimal(tiger2)
    enclosure2.addAnimal(tiger3)

    animalStat = zoo1.getAnimalStat()

    expected = {
        'total_num_animals_per_species': {'tiger': 1, 'tiger2': 2},
        'avg_num_animals_per_enclosure': 3 / 2,
        'num_enclosures_with_different_species': 1,
        'avail_space_per_animal_in_enclosure': {enclosure1.enclosure_id: 5 / 2,
                                                enclosure2.enclosure_id: 10 / 1}
    }

    assert (animalStat == expected)


def test_addEnclosure(zoo1, enclosure1):
    zoo1.addEnclosure(enclosure1)
    # Is the enclosure in the list
    assert (enclosure1 in zoo1.enclosures)
    # Checks the length of the list of enclosures
    assert (len(zoo1.enclosures) == 1)


def test_getEnclosure(zoo1, enclosure1):
    zoo1.addEnclosure(enclosure1)
    enclosure = zoo1.getEnclosure(enclosure1.enclosure_id)

    assert (enclosure == enclosure1)


def test_removeEnclosure(zoo1, enclosure1, enclosure2, tiger1):
    zoo1.addAnimal(tiger1)
    zoo1.addEnclosure(enclosure1)
    zoo1.addEnclosure(enclosure2)
    enclosure1.addAnimal(tiger1)
    # Checks the length of the list of enclosures
    assert (len(zoo1.enclosures) == 2)

    zoo1.removeEnclosure(enclosure1)
    # Checks the length of the list of enclosures
    assert (len(zoo1.enclosures) == 1)
    # Is the animal in the list of other enclosure
    assert (tiger1 in enclosure2.animals)


def test_addEmployee(zoo1, caretaker1):
    zoo1.addEmployee(caretaker1)
    # Is the caretaker in the list
    assert (caretaker1 in zoo1.employees)
    # Checks the length of the list of caretakers
    assert (len(zoo1.employees) == 1)


def test_getEmployee(zoo1, caretaker1):
    zoo1.addEmployee(caretaker1)
    caretaker = zoo1.getEmployee(caretaker1.employee_id)

    assert (caretaker == caretaker1)


def test_removeEmployee(zoo1, caretaker1, caretaker2, tiger1):
    zoo1.addEmployee(caretaker1)
    zoo1.addEmployee(caretaker2)
    zoo1.addAnimal(tiger1)
    caretaker1.addAnimal(tiger1)
    # Checks the length of the list of caretakers
    assert (len(zoo1.employees) == 2)
    zoo1.removeEmployee(caretaker1)
    # Checks the length of the list of caretakers
    assert (len(zoo1.employees) == 1)
    # Is the animal in the list of other caretaker
    assert (tiger1 in caretaker2.list_of_animals)


def test_getEmployeeStat(zoo1, caretaker1, caretaker2, tiger1, tiger2, tiger3):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addAnimal(tiger3)
    zoo1.addEmployee(caretaker1)
    zoo1.addEmployee(caretaker2)

    caretaker1.addAnimal(tiger1)
    caretaker1.addAnimal(tiger2)
    caretaker2.addAnimal(tiger3)

    employeeStat = zoo1.getEmployeeStat()

    expected = {'min': 1,
                'max': 2,
                'average_number': 3 / 2}

    assert (employeeStat == expected)


def test_createCleaningPlan(zoo1, enclosure1, caretaker1):
    zoo1.addEmployee(caretaker1)
    zoo1.addEnclosure(enclosure1)
    enclosure1.clean()

    zoo1.createCleaningPlan()

    next = enclosure1.cleaning_record[0] + datetime.timedelta(days=3)
    next = f"{next.day}.{next.month}.{next.year}"

    expected = {enclosure1.enclosure_id:
                    ["Next date for cleaning: " + next,
                     "Responsible employee: " + caretaker1.employee_id]}

    assert (expected == zoo1.cleaning_plan)


def test_createMedicalPlan(zoo1, tiger1):
    zoo1.addAnimal(tiger1)
    tiger1.vet()

    zoo1.createMedicalPlan()

    next = tiger1.vet_record[0] + datetime.timedelta(days=35)
    next = f"{next.day}.{next.month}.{next.year}"

    expected = {tiger1.animal_id: "Next date for medical check-up: " + next}

    assert (expected == zoo1.medical_plan)


def test_createFeedingPlan(zoo1, tiger1, caretaker1):
    zoo1.addAnimal(tiger1)
    zoo1.addEmployee(caretaker1)
    tiger1.feed()

    zoo1.createFeedingPlan()

    next = tiger1.feeding_record[0] + datetime.timedelta(days=2)
    next = f"{next.day}.{next.month}.{next.year}"

    expected = {tiger1.animal_id:
                    ["Next date for feeding: " + next,
                     "Responsible employee: " + caretaker1.employee_id]}

    assert (expected == zoo1.feeding_plan)
