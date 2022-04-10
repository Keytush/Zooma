import pytest

from animal import Animal
from zoo import Zoo
from enclosure import Enclosure


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


def test_addAnimal(zoo1, tiger1, tiger2, enclosure1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addEnclosure(enclosure1)
    # Is the animal in the list
    assert (enclosure1 in zoo1.enclosures)
    enclosure1.addAnimal(tiger1)
    enclosure1.addAnimal(tiger2)
    # Checks the length of the list of animals
    assert (len(enclosure1.animals) == 2)


def test_removeAnimal(zoo1, tiger1, tiger2, enclosure1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addEnclosure(enclosure1)

    enclosure1.addAnimal(tiger1)
    enclosure1.addAnimal(tiger2)
    # Checks the length of the list of animals
    assert (len(enclosure1.animals) == 2)

    enclosure1.removeAnimal(tiger2)
    # Checks the length of the list of animals
    assert (len(enclosure1.animals) == 1)


def test_cleanEnclosure(zoo1, enclosure1):
    zoo1.addEnclosure(enclosure1)

    enclosure1.clean()
    # Checks the length of the cleaning record
    assert (len(enclosure1.cleaning_record) == 1)

    enclosure1.clean()
    # Checks the length of the cleaning record
    assert (len(enclosure1.cleaning_record) == 2)
