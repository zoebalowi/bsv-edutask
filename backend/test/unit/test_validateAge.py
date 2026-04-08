import pytest
from src.util.helpers import ValidationHelper

@pytest.mark.unit
def test_validateAge():
    result = ValidationHelper.validateAge(25)
    assert result == True