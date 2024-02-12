"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file.
Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

client = app.test_client()

class CounterTest(TestCase):
    """Counter tests"""

    def test_create_a_counter(self):
        """It should create a counter"""
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update an existing counter"""
        # create counter
        result = client.post('/counters/fooUpdate')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # get baseline
        baselineGet = client.get('/counters/fooUpdate')
        dataGet = baselineGet.json
        baseline = dataGet['fooUpdate']
        # update counter
        result = client.put('/counters/fooUpdate')
        data = result.json
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(data['fooUpdate'], baseline+1)
        # try non existing counter
        result = client.put('/counters/noNameCounter')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)


    def test_read_a_counter(self):
        """It should read an existing counter"""
        # create counter
        result = client.post('/counters/fooRead')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # Read the counter
        result = client.get('/counters/fooRead')
        data = result.json
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(data['fooRead'], 0)
        # try non existing counter
        result = client.get('/counters/noNameCounter')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)