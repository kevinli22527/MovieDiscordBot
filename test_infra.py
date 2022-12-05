import pytest
from mongo_initialization import *
from mongo_ratings import *
from mongo_users import *
from mongo_turns import *
from mongo_watch_lists import *

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

# for testing the clear watch list function
def test_6():
    initialize_test_database()
    assert len(getUserWatchList("656333371827421225")) == 3
    assert len(getUserWatchList("279423302408339456")) == 2
    clear_watch_list("656333371827421225")
    assert len(getUserWatchList("656333371827421225")) == 0
    clear_watch_list("279423302408339456")
    assert len(getUserWatchList("279423302408339456")) == 0

# run this after all tests have been finished
@pytest.fixture(scope="module", autouse=True)
def teardown():
    initialize_test_database()  # reinitialize the database to a blank slate