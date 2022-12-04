import pytest
from mongo_utility import *

# run before tests start
@pytest.fixture(scope="module", autouse=True)
def setup():
    initialize_test_database()

def test_1():
    assert isInUserWatchList("656333371827421225", "Ella Enchanted")

def test_2():
    assert isInUserWatchList("656333371827421225", "Jurassic Park")

def test_3():
    assert isInUserWatchList("279423302408339456", "Mad Max")

def test_4():
    assert isInUserWatchList("279423302408339456", "Transformers")

def test_5():
    initialize_test_database()
    removeFromUserWatchList("656333371827421225", "Jurassic Park")
    assert not isInUserWatchList("656333371827421225", "Jurassic Park")
    removeFromUserWatchList("279423302408339456", "Mad Max")
    assert not isInUserWatchList("279423302408339456", "Mad Max")