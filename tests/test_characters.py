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


def test_character_from_rank():
    warrior = Warrior.from_rank("Warrior", 2)
    assert str(
        warrior) == "<Name:Warrior Fighting Prowess=8 Psychic Ability=6 Awareness=6 Endurance=12>"

    sage = Sage.from_rank("Sage", 2)
    assert str(
        sage) == "<Name:Sage Fighting Prowess=7 Psychic Ability=7 Awareness=6 Endurance=10>"

    warrior8 = Warrior.from_rank("Warrior", 8)
    assert str(
        warrior8) == "<Name:Warrior Fighting Prowess=9 Psychic Ability=7 Awareness=7 Endurance=48>"

    sage8 = Sage.from_rank("Sage", 8)
    assert str(
        sage8) == "<Name:Sage Fighting Prowess=8 Psychic Ability=8 Awareness=7 Endurance=40>"


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


def test_item_stored(sage, warrior):
    assert len(sage.items_carried) == len(
        [i for i in vars(sage.__class__).values() if isinstance(i, Equipable)])
    assert len(warrior.items_carried) == len(
        [i for i in vars(warrior.__class__).values() if isinstance(i, Equipable)])


def test_that_character_can_only_carry_one_piece_of_armour(warrior):
    initial_no_items_carried = len(warrior.items_carried)
    new_armour = Armour('ringmail', damage_reduction=2)
    warrior.armour = new_armour
    assert warrior.armour.damage_reduction == 2
    assert len(warrior.items_carried) == initial_no_items_carried
