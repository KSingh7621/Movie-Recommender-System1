import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4df88e6087a1efea22b95b33881e8668&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']


movies_list = pickle.load(open('movies.pkl','rb'))
movies = movies_list['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))


st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Select the movie",movies)


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list_sel = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list_sel:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1,col2,col3,col4,col5 = st.columns(5,gap = "medium")
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

    col6, col7, col8, col9, col10 = st.columns(5, gap = "medium")
    with col6:
        st.text(names[5])
        st.image(posters[5])
    with col7:
        st.text(names[6])
        st.image(posters[6])
    with col8:
        st.text(names[7])
        st.image(posters[7])
    with col9:
        st.text(names[8])
        st.image(posters[8])
    with col10:
        st.text(names[9])
        st.image(posters[9])
