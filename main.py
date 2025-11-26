# main.py (Оновлений)

import sys
import time
# !!! Змініть імпорт:
from data_access.wikidata_client import DBpediaClient 

def run_console_test():
    """
    Консольна функція для тестування модуля доступу до даних (DAL) 
    з використанням DBpedia.
    """
    
    print("=========================================")
    print("   Тест: З'єднання з DBpedia та DAL      ")
    print("=========================================")
    
    # !!! Створюємо екземпляр DBpediaClient:
    client = DBpediaClient()
    
    start_time = time.time()

    # 1. Тест: Отримання Топ-5 міст
    print("\n--- 1. Тест: Топ-5 найбільших міст Каліфорнії (DBpedia) ---")
    
    try:
        cities = client.get_top_cities(limit=5)
        
        if cities:
            print(f"Успіх! Отримано {len(cities)} міст.")
            for i, city in enumerate(cities):
                print(f"  {i+1}. Місто: {city['city']}, Населення: {city['population']:,} осіб, Координати: {city['coordinates']}")
        else:
            print("Помилка: Запит повернув порожній список. Можливі причини: помилка SPARQL, відсутність даних, або таймаут.")
    except Exception as e:
        print(f"Критична помилка під час виконання запиту get_top_cities: {e}")
        
    # 2. Тест: Отримання 10 університетів
    print("\n--- 2. Тест: 10 університетів Каліфорнії (DBpedia) ---")
    
    try:
        universities = client.get_universities()
        
        if universities:
            print(f"Успіх! Отримано {len(universities)} університетів.")
            for i, uni in enumerate(universities):
                print(f"  {i+1}. Університет: {uni['name']}")
        else:
            print("Помилка: Запит повернув порожній список.")
    except Exception as e:
        print(f"Критична помилка під час виконання запиту get_universities: {e}")

    end_time = time.time()
    print(f"\nЗагальний час виконання тестів DAL: {end_time - start_time:.2f} секунд.")
    # 3. Тест: 10 пам'яток
    print("\n--- 3. Тест: 10 визначних місць (пам'ятки) ---")
    try:
        landmarks = client.get_landmarks()
        
        if landmarks:
            print(f"Успіх! Отримано {len(landmarks)} пам'яток.")
            for i, landmark in enumerate(landmarks):
                print(f"  {i+1}. Пам'ятка: {landmark['name']}")
        else:
            print("Помилка: Запит пам'яток повернув порожній список.")
    except Exception as e:
        print(f"Критична помилка під час виконання запиту get_landmarks: {e}")


    end_time = time.time()
    print(f"\n=========================================")
    print(f"Загальний час виконання тестів DAL: {end_time - start_time:.2f} секунд.")

if __name__ == "__main__":
    run_console_test()