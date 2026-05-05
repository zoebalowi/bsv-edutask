import pytest
from pymongo import MongoClient
from src.util.dao import DAO
from pymongo.errors import WriteError

from unittest.mock import MagicMock, patch


@pytest.fixture
def mocked_validator():
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "description"],
            "properties": {
                "name": {
                    "bsonType": "string"
                },
                "description": {
                    "bsonType": "string"
                }
            }
        }
    }


@pytest.fixture
def create_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.edutask
    collection_name = "test_task_create"

    db.drop_collection(collection_name)

    yield db

    db.drop_collection(collection_name)
    client.close()


def test_create_valid_input(create_db, mocked_validator):
    db = create_db
    collection_name = "test_task_create"

    with patch("src.util.dao.getValidator", return_value=mocked_validator):
        dao = DAO(collection_name)
    data = {
        "name": "Test",
        "description": "jewniuw"
    }

    result = dao.create(data)
    assert result["name"] == "Test"
    assert result["description"] == "jewniuw"

    db_result = db[collection_name].find_one({"name": "Test"})
    assert db_result is not None


def test_validator_reject(create_db, mocked_validator):
    db = create_db
    collection_name = "test_task_create"

    with patch("src.util.dao.getValidator", return_value=mocked_validator):
        dao = DAO(collection_name)

    invalid_data = {
        "name": 123,
        "description": "Not string"
    }

    with pytest.raises(WriteError):
        dao.create(invalid_data)
    db_result = db[collection_name].find_one({
        "description": "Not string"
    })
    assert db_result is None


def test_mongodb_fail():
    dao = DAO("task")
    dao.collection = MagicMock()
    dao.collection.insert_one.side_effect = Exception()

    data = {
        "name": "Test",
        "description": "kjwniprn"
    }
    with pytest.raises(Exception):
        dao.create(data)


def test_create_input_not_dictionary():
    dao = DAO("task")
    dao.collection = MagicMock()
    data = 1

    with pytest.raises(Exception):
        dao.create(data)
    
