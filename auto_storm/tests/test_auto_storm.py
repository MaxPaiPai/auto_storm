from auto_storm import __version__
from auto_storm import *

def test_version():
    assert __version__ == '0.0.1'


def test_bmi():
     results = bmi(78, 1.75)
     assert results == 25.0