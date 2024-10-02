import streamlit as st
import pickle
import requests


st.set_page_config(layout="wide")

# adding custom padding
st.markdown(
    """
    <style>
    /* Adjust padding for the entire main container */
    .main {
        padding-top: 0px;
        padding-left: 200px;  /* Set custom padding (adjust as needed) */
        padding-right: 200px;
    }
    .stContainer {
            padding-top: 0;  /* Adjust this value */
    }
    h1 {
        margin-top: 0;  /* Remove top margin for title */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_poster_and_imdb(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4df88e6087a1efea22b95b33881e8668&language=en-US'.format(movie_id))
    data = response.json()
    poster_path =  "https://image.tmdb.org/t/p/w500"+data['poster_path']
    imdb_id = data['imdb_id']  # Get the IMDb ID
    imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
    overview = data.get('overview', 'No overview available.')
    release_year = data['release_date'][:4]
    imdb_rating = data.get('vote_average', 'N/A')
    genres = [genre['name'] for genre in data.get('genres', [])]
    genres = ', '.join(genres) if genres else 'Genres not available'

    # Fetch movie credits (to get director and cast)
    credits_response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=4df88e6087a1efea22b95b33881e8668&language=en-US')
    credits_data = credits_response.json()
    director = [crew['name'] for crew in credits_data['crew'] if crew['job'] == 'Director']
    director = director[0] if director else 'Director not available'
    return poster_path, imdb_url, overview, release_year, imdb_rating,genres,director


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
    recommended_movies_imdb = []
    for i in movies_list_sel:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        poster_path, imdb_url, overview, release_year, imdb_rating,genre,director = fetch_poster_and_imdb(movie_id)
        recommended_movies_poster.append(poster_path)
        recommended_movies_imdb.append(imdb_url)

    return recommended_movies, recommended_movies_poster, recommended_movies_imdb
    # return recommended_movies, recommended_movies_poster




# Display recommendations when button is clicked
if st.button('Recommend'):

    # Fetch selected movie details (poster, IMDb URL, and overview)
    selected_movie_id = movies_list[movies_list['title'] == selected_movie_name].iloc[0].movie_id
    selected_poster, selected_imdb_url,selected_overview, selected_release_year, selected_imdb_rating,selected_genres,selected_director = fetch_poster_and_imdb(selected_movie_id)

    # Display selected movie details at the top
    st.subheader(f"Selected Movie: {selected_movie_name}")
    col1, col2 = st.columns([1, 2])  # Two columns: one for poster, one for info
    with col1:
        # Display the movie poster
        st.markdown(
            f'<a href="{selected_imdb_url}" target="_blank">'
            f'<img src="{selected_poster}" width="{180}" height="{230}" style="object-fit: cover;"/></a>',
            unsafe_allow_html=True
        )
    with col2:
        # Display the overview and IMDb link
        st.markdown(f"**IMDb Rating:** {selected_imdb_rating}/10")
        st.markdown(f"**Release Year:** {selected_release_year}")
        st.markdown(f"**Overview:** {selected_overview}")
        st.markdown(f"**Genre:** {selected_genres}")
        st.markdown(f"**Director:** {selected_director}")
        st.markdown(f"[View on IMDb]({selected_imdb_url})", unsafe_allow_html=True)

    # Get recommendations
    st.text("")
    st.subheader(f"Recommended Movies:")
    st.text("")
    names, posters, imdb_urls = recommend(selected_movie_name)
    image_width = 180  # Adjust as needed
    image_height = 230  # Adjust as needed (to maintain aspect ratio)

    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.text(names[i])
            # Use st.markdown for clickable image with fixed width and height
            st.markdown(
                f'<a href="{imdb_urls[i]}" target="_blank">'
                f'<img src="{posters[i]}" width="{image_width}" height="{image_height}" style="object-fit: cover;"/></a>',
                unsafe_allow_html=True
            )
    st.text("")
    col6, col7, col8, col9, col10 = st.columns(5, gap="medium")
    for i, col in enumerate([col6, col7, col8, col9, col10], start=5):
        with col:
            st.text(names[i])
            # Use st.markdown for clickable image with fixed width and height
            st.markdown(
                f'<a href="{imdb_urls[i]}" target="_blank">'
                f'<img src="{posters[i]}" width="{image_width}" height="{image_height}" style="object-fit: cover;"/></a>',
                unsafe_allow_html=True
            )

## api key   4df88e6087a1efea22b95b33881e8668