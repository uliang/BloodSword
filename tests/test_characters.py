import pytest
from bloodsword.characters.sage import Sage
from bloodsword.characters.warrior import Warrior
from bloodsword.descriptors.armour import Armour


@pytest.fixture
def warrior():
    return Warrior("Warrior", rank=2)


@pytest.fixture
def sage():
    return Sage("Sage", rank=2)


def test_character_initialization(warrior, sage):
    assert str(
        warrior) == "<Name:Warrior Fighting Prowess=8 Psychic Ability=6 Awareness=6 Endurance=12>"
    assert str(
        sage) == "<Name:Sage Fighting Prowess=7 Psychic Ability=7 Awareness=6 Endurance=10>"


def test_endurance_cannot_exceed_max(warrior):
    warrior.endurance = 13
    assert warrior.endurance == 12


def test_endurance_increments(warrior):
    warrior.endurance = 10
    warrior.endurance += 1
    assert warrior.endurance == 11


def test_endurance_increments_beyond_max(warrior):
    warrior.endurance = 10
    warrior.endurance += 5
    assert warrior.endurance == 12


def test_attribute_decrements(warrior, sage):
    sage.endurance -= 1
    assert sage.endurance == 9

    warrior.endurance -= 1
    assert warrior.endurance == 11

    sage.psychic_ability -= 2
    assert sage.psychic_ability == 5


def test_attribute_decrement_clips_at_zero(sage, warrior):
    sage.psychic_ability -= 10
    assert sage.psychic_ability == 0

    warrior.endurance -= 20
    assert warrior.endurance == 0


def test_that_character_can_only_carry_one_piece_of_armour(warrior):
    initial_no_items_carried = len(warrior.items_carried)
    new_armour = Armour('ringmail', damage_reduction=2)
    warrior.armour = new_armour
    assert warrior.armour.damage_reduction == 2
    assert len(warrior.items_carried) == initial_no_items_carried
