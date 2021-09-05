from unittest import mock

import pytest
from src.data.availability_dao import AvailabilityDao
import sys, os

# myPath = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, myPath + '/../')
from src.models.website_availability_item import WebsiteAvailabilityItem

""" Inspired by https://github.com/aiven/aiven-examples/blob/master/tests/test_aiven_examples.py """

test_uri = 'XXX'
test_table_name = 'test'
test_limit = 10
test_query_result = [("test_item_1", "test_item_2")]
test_items = [(WebsiteAvailabilityItem("test", 200, 123, {'[a-z]+': True}))]
test_json_dict = {
    "https://yle.fi/": [
        "(Urheiluu)",
        "[a-z]+"
    ]
}


def test_producer():
    # gets the availability thing
    pass


def test_consumer():
    # Calls db save
    pass


def test_it_saves_item():
    with mock.patch('psycopg2.connect') as mock_connect:
        # mock_connect().cursor.return_value.executemany.return_value = test_query_result
        dao = AvailabilityDao(test_uri, test_table_name)
        result = dao.save(test_items)
        # assert result == test_query_result


def test_it_can_fetch_data():
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_connect().cursor.return_value.fetchall.return_value = test_query_result
        dao = AvailabilityDao(test_uri, test_table_name)
        result = dao.get_recent_updates(test_limit)
        assert result == test_query_result


def test_it_reads_availability_json_file():
    pass


def test_it_normalizes_url():
    pass
