# data_access/dbpedia_client.py (або оновлений data_access/wikidata_client.py)

from SPARQLWrapper import SPARQLWrapper, JSON

class DBpediaClient:
    """Клієнт для взаємодії з ендпойнтом DBpedia SPARQL."""
    
    # Ресурс DBpedia для штату Каліфорнія
    CALIFORNIA_RESOURCE = "California"
    # Ендпойнт SPARQL для DBpedia
    DBPEDIA_ENDPOINT = "http://dbpedia.org/sparql" # Основний ендпойнт DBpedia

    def __init__(self):
        """Ініціалізація SPARQLWrapper для DBpedia."""
        self.sparql = SPARQLWrapper(self.DBPEDIA_ENDPOINT)
        self.sparql.setReturnFormat(JSON)

    def _execute_query(self, query):
        """Приватний метод для виконання запиту та повернення результатів."""
        self.sparql.setQuery(query)
        try:
            # Встановлення таймауту на 30 секунд (може допомогти з повільним з'єднанням)
            self.sparql.setTimeout(30) 
            results = self.sparql.query().convert()
            return results["results"]["bindings"]
        except Exception as e:
            print(f"Помилка виконання SPARQL-запиту до DBpedia: {e}")
            return []

    def get_top_cities(self, limit=5):
        """
        Запит: Повертає найбільші міста Каліфорнії за чисельністю населення з DBpedia.
        Властивості DBpedia: dbo:city, dbo:populationTotal, geo:lat/geo:long.
        """
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

        SELECT DISTINCT ?cityLabel (xsd:integer(?population) AS ?Population) ?lat ?long
        WHERE 
        {{
          ?city dbo:subdivision dbr:{self.CALIFORNIA_RESOURCE} . # Місто, що є підрозділом Каліфорнії
          ?city a dbo:City .
          ?city dbo:populationTotal ?population . # Загальне населення
          
          OPTIONAL {{ ?city geo:lat ?lat ; geo:long ?long . }} # Географічні координати
          
          ?city rdfs:label ?cityLabel .
          FILTER (lang(?cityLabel) = 'en' || lang(?cityLabel) = 'uk')
          
          # Фільтруємо нечислові або некоректні значення населення
          FILTER(datatype(?population) = xsd:integer || datatype(?population) = xsd:nonNegativeInteger)
        }}
        ORDER BY DESC(?Population)
        LIMIT {limit}
        """
        results = self._execute_query(query)
        
        # Обробка результатів
        processed_results = []
        for binding in results:
            pop_value = binding.get("Population", {}).get("value")
            
            # DBpedia повертає широту/довготу окремо
            coords = f"{binding.get('lat', {}).get('value', 'N/A')}, {binding.get('long', {}).get('value', 'N/A')}"
            
            processed_results.append({
                "city": binding.get("cityLabel", {}).get("value", "N/A"),
                "population": int(pop_value) if pop_value and pop_value.isdigit() else 0,
                "coordinates": coords
            })
        return processed_results

    def get_universities(self):
        """
        Запит: Повертає найбільші університети Каліфорнії з DBpedia.
        Властивості DBpedia: dbo:state, dbo:type (University).
        """
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?uniLabel ?uni
        WHERE 
        {{
          ?uni dbo:state dbr:{self.CALIFORNIA_RESOURCE} . # Університет розташований у Каліфорнії
          ?uni a dbo:University .
          ?uni rdfs:label ?uniLabel .
          
          FILTER (lang(?uniLabel) = 'en' || lang(?uniLabel) = 'uk')
        }}
        LIMIT 10
        """
        results = self._execute_query(query)
        
        processed_results = []
        for binding in results:
            processed_results.append({
                "name": binding.get("uniLabel", {}).get("value", "N/A"),
                "uri": binding.get("uni", {}).get("value", "#")
            })
        return processed_results