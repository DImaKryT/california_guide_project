# app.py

import os
from flask import Flask, render_template
# !!! ІМПОРТУЄМО DBpediaClient:
from data_access.wikidata_client import DBpediaClient

app = Flask(__name__)
# !!! Створюємо екземпляр DBpediaClient
client = DBpediaClient()

@app.route('/')
def index():
    """
    Основний маршрут ('/'). 
    Отримує дані з DAL (DBpedia) та передає їх для відображення.
    """
    
    # 1. Отримання даних з Data Access Layer
    cities = client.get_top_cities(limit=5)
    universities = client.get_universities()
    landmarks = client.get_landmarks()
    
    # 2. Передача даних до шаблону для візуалізації
    return render_template(
        'index.html',
        cities=cities,
        universities=universities,
        landmarks=landmarks,
        title="Гід штату Каліфорнія (DBpedia Project)"
    )

if __name__ == '__main__':
    app.run(debug=True)