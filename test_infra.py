import pytest
from mongo_utility import *

def test_1():
    assert isInUserWatchList("656333371827421225", "Ella Enchanted")

def test_2():
    assert isInUserWatchList("656333371827421225", "Jurassic Park")

def test_3():
    assert isInUserWatchList("279423302408339456", "Mad Max")

def test_4():
    assert isInUserWatchList("279423302408339456", "Transformers")