import pytest

from animal import Animal
from zoo import Zoo
from enclosure import Enclosure

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


def test_addAnimal(zoo1, tiger1, tiger2, enclosure1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addEnclosure(enclosure1)
    assert (enclosure1 in zoo1.enclosures)
    enclosure1.addAnimal(tiger1)
    enclosure1.addAnimal(tiger2)

    assert (len(enclosure1.animals) == 2)

def test_removeAnimal(zoo1, tiger1, tiger2, enclosure1):
    zoo1.addAnimal(tiger1)
    zoo1.addAnimal(tiger2)
    zoo1.addEnclosure(enclosure1)

    enclosure1.addAnimal(tiger1)
    enclosure1.addAnimal(tiger2)

    assert (len(enclosure1.animals) == 2)

    enclosure1.removeAnimal(tiger2)

    assert (len(enclosure1.animals) == 1)

def test_cleanEnclosure(zoo1, enclosure1):
    zoo1.addEnclosure(enclosure1)

    enclosure1.clean()

    assert (len(enclosure1.cleaning_record) == 1)

    enclosure1.clean()

    assert (len(enclosure1.cleaning_record) == 2)