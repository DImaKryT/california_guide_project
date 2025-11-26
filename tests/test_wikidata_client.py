# tests/test_wikidata_client.py

import unittest
from unittest.mock import patch, MagicMock
from data_access.wikidata_client import DBpediaClient

# Імітація відповіді SPARQL для тестів
MOCK_CITY_RESULTS = {
    "results": {
        "bindings": [
            {
                "cityLabel": {"value": "Лос-Анджелес", "xml:lang": "uk"},
                "population": {"value": "3898747", "datatype": "http://www.w3.org/2001/XMLSchema#integer"},
                "coordinates": {"value": "Point(-118.243685 34.052234)"}
            },
            {
                "cityLabel": {"value": "San Diego", "xml:lang": "en"},
                "population": {"value": "1386932", "datatype": "http://www.w3.org/2001/XMLSchema#integer"},
                "coordinates": {"value": "Point(-117.161084 32.715738)"}
            }
        ]
    }
}

MOCK_UNI_RESULTS = {
    "results": {
        "bindings": [
            {"uniLabel": {"value": "Stanford University"}, "uni": {"value": "http://www.wikidata.org/entity/Q41506"}},
            {"uniLabel": {"value": "University of California, Berkeley"}, "uni": {"value": "http://www.wikidata.org/entity/Q168756"}}
        ]
    }
}


class TestWikidataClient(unittest.TestCase):

    def setUp(self):
        """Ініціалізація клієнта перед кожним тестом."""
        self.client = DBpediaClient()

    @patch('data_access.wikidata_client.SPARQLWrapper.query')
    def test_get_top_cities_returns_correct_format(self, mock_query):
        """Перевіряє, чи метод get_top_cities повертає структуровані дані."""
        
        # Мокінг (імітація) відповіді від SPARQL
        mock_convert = MagicMock()
        mock_convert.convert.return_value = MOCK_CITY_RESULTS
        mock_query.return_value = mock_convert

        cities = self.client.get_top_cities(limit=2)

        # Перевірка формату та вмісту
        self.assertIsInstance(cities, list)
        self.assertEqual(len(cities), 2)
        
        first_city = cities[0]
        self.assertIn("city", first_city)
        self.assertIn("population", first_city)
        self.assertIn("coordinates", first_city)
        
        # Перевірка, що населення перетворено на ціле число (int)
        self.assertIsInstance(first_city['population'], int)
        self.assertEqual(first_city['city'], "Лос-Анджелес")

    @patch('data_access.wikidata_client.SPARQLWrapper.query')
    def test_get_universities_returns_list(self, mock_query):
        """Перевіряє, чи метод get_universities повертає список."""
        
        # Мокінг (імітація) відповіді від SPARQL
        mock_convert = MagicMock()
        mock_convert.convert.return_value = MOCK_UNI_RESULTS
        mock_query.return_value = mock_convert
        
        universities = self.client.get_universities()
        
        # Перевірка формату
        self.assertIsInstance(universities, list)
        self.assertEqual(len(universities), 2)
        self.assertIn("name", universities[0])
        self.assertIn("uri", universities[0])

if __name__ == '__main__':
    # Запускається командою: python -m unittest tests/test_wikidata_client.py
    unittest.main()