from bloodsword.utils import roll_dice
import random
import pytest


@pytest.fixture
def mock_random_choice(monkeypatch):
    def mockreturn(arr, k):
        return [max(arr)]*k

    monkeypatch.setattr(random, 'choices', mockreturn)


def test_roll_dice_string_input(mock_random_choice):
    assert roll_dice('2d6+1') == 13
    assert roll_dice('2d6') == 12
    assert roll_dice('3d6') == 18
    assert roll_dice('1d4') == 4
    assert roll_dice('d4') == 4
    assert roll_dice('1d20+10') == 30
    assert roll_dice('10d4') == 40
    assert roll_dice('100d100') == 100*100


def test_roll_dice_int_input(mock_random_choice):
    assert roll_dice(n=2, d=6, modifier=1) == 13
    assert roll_dice(n=2, d=6, modifier=0) == 12
    assert roll_dice(n=2, d=6) == 12

def test_roll_dice_invalid_input(mock_random_choice):
    with pytest.raises(ValueError) as exec:
        roll_dice('dd4')
    assert "Incorrect dice specification" in str(exec.value)

    with pytest.raises(ValueError) as exec:
        roll_dice()
    assert "No dice specified" in str(exec.value)

    with pytest.raises(ValueError) as exec: 
        roll_dice(n=0, d=6, modifier=0)
    assert "Incorrect dice specification" in str(exec.value)