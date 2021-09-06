from unittest import mock

from src.data.availability_dao import AvailabilityDao
from src.models.website_availability_item import WebsiteAvailabilityItem
from src.processing.website_availability_processor import website_availability_processor
from src.service.producer_service import run

test_uri = 'XXX'
test_table_name = 'test'
test_limit = 10
test_query_result = [("test_item_1", "test_item_2")]
test_availability_items = [
    (WebsiteAvailabilityItem("test", 200, 123, {'[a-z]+': True, "(Urheiluu)": True}))]
test_json_dict = {
    "https://yle.fi/": [
        "(Urheiluu)",
        "[a-z]+"
    ]
}
test_html = "<!DOCTYPE html><html><body><h1>Urheiluu<h1></body></html>"


class TestWebsiteAvailabilityMonitor:
    def test_producer(self):
        with mock.patch('src.service.producer_service.AvailabilityProducer') as mock_producer, \
                mock.patch('src.service.producer_service.website_availability_processor') as mock_processor:
            mock_processor.return_value = test_availability_items
            run(mock_producer, 0)
            mock_producer.send.assert_called_with(test_availability_items)

    def test_website_processor(self):
        with mock.patch('os.path'), mock.patch('json.load') as mock_json_load, mock.patch(
                'requests.get') as mock_requests:
            mock_json_load.return_value = test_json_dict
            mock_requests().content = test_html
            mock_requests().elapsed.microseconds = 123
            mock_requests().status_code = 200
            assert website_availability_processor()[0].regex_pattern_matches == test_availability_items[
                0].regex_pattern_matches
            assert website_availability_processor()[0].status_code == test_availability_items[0].status_code
            assert website_availability_processor()[0].response_time == test_availability_items[0].response_time

    def test_save_method_executes_many_and_commits(self):
        with mock.patch('psycopg2.connect') as mock_connect:
            dao = AvailabilityDao(test_uri, test_table_name)
            dao.save(test_availability_items)
            mock_connect().cursor().executemany.assert_called()
            mock_connect().commit.assert_called()

    def test_it_fetches_data(self):
        with mock.patch('psycopg2.connect') as mock_connect:
            mock_connect().cursor.return_value.fetchall.return_value = test_query_result
            dao = AvailabilityDao(test_uri, test_table_name)
            result = dao.get_recent_updates(test_limit)
            assert result == test_query_result
