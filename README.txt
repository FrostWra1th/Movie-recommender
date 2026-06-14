# 🎬 Movie Recommendation System

Веб-приложение на базе Streamlit, которое рекомендует 5 похожих фильмов на основе выбранного. 
Использует алгоритм Item-Based коллаборативной фильтрации (NearestNeighbors) и датасет MovieLens.

## Как запустить локально

1. Склонируйте репозиторий.
2. Установите зависимости: `pip install -r requirements.txt`
3. Скачайте датасет MovieLens (файлы movies.csv и ratings.csv) и положите их в папку `data/`.
4. Запустите предварительную обработку данных: `python prepare_data.py`
5. Запустите приложение: `streamlit run app.py`