import pytest
from src.models.item import Item as item

def test_item_description_return_string():
    item1 = item(name="Sword", description="A sword for fighting")
    assert type(item1.description) == str

def test_item_name_return_string():
    item1 = item(name="Sword", description="A sword for fighting")
    assert type(item1.name) == str

def test_item_status_return_boolean():
    item1 = item(name="Sword", description="A sword for fighting", status=True)
    assert type(item1.status) == bool

def test_item_status_return_boolean_default_false():
    item1 = item(name="Sword", description="A sword for fighting")
    assert item1.status == False

def test_item_name_if_empty_gives_error():
    with pytest.raises(ValueError):
        item1 = item(name="", description="A sword for fighting")

def test_item_has_id():
    item1 = item(name="Sword", description="A sword for fighting")
    assert hasattr(item1, "id") == True
