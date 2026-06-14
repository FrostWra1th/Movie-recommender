import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import sys
from streamlit.web import cli as stcli
from streamlit.runtime import exists

# Настройка страницы
st.set_page_config(page_title="Рекомендации фильмов", page_icon="🎬")

st.title("🎬 Рекомендательная система фильмов")
st.markdown("Выберите фильм, и система предложит 5 похожих на основе оценок пользователей (MovieLens 100k).")


# --- 1. ЗАГРУЗКА И КЭШИРОВАНИЕ ДАННЫХ ---
@st.cache_data
def load_data():
    ratings = pd.read_csv('data/ratings.csv')
    movies = pd.read_csv('data/movies.csv')
    df = pd.merge(ratings, movies, on='movieId')
    movie_matrix = df.pivot_table(index='title', columns='userId', values='rating').fillna(0)

    return movie_matrix, movies


try:
    with st.spinner():
        movie_matrix, movies_df = load_data()
except FileNotFoundError:
    st.error("Файлы данных не найдены")
    st.stop()


@st.cache_resource
def train_model(matrix):
    # Используем косинусное сходство и алгоритм brute для точного поиска
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6)
    model_knn.fit(matrix.values)
    return model_knn


model = train_model(movie_matrix)


movie_list = movie_matrix.index.tolist()
selected_movie = st.selectbox("Выберите фильм, который вам нравится:", movie_list)

if st.button("Найти похожие"):

    query_index = movie_list.index(selected_movie)

    distances, indices = model.kneighbors(movie_matrix.iloc[query_index, :].values.reshape(1, -1), n_neighbors=6)

    st.subheader(f"Топ-5 фильмов, похожих на «{selected_movie}»:")

    for i in range(1, len(distances.flatten())):
        recommended_movie = movie_matrix.index[indices.flatten()[i]]

        similarity = (1 - distances.flatten()[i]) * 100


        st.write(f"**{i}. {recommended_movie}** — сходство: {similarity:.1f}%")



if __name__ == "__main__":

    if not exists():
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())