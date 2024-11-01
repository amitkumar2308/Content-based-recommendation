import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f8ff7e6827635767bf5a859edcaf9acb&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    # Locate the index of the movie by filtering for the title
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    # Get top 5 similar movies (excluding the input movie itself)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    # Print recommended movie titles
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load the data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.markdown("<h1 style='text-align: center; font-size: 36px; color: #ff6347;'>Movie Recommender System</h1>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Select the movie',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Create a container for the recommended movies
    with st.container():
        st.write("<h2 style='text-align: center; color: #333;'>Recommended Movies</h2>", unsafe_allow_html=True)

        # Create a grid layout for displaying movie cards
        cols = st.columns(5)
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.markdown(
                    f"""
                    <div style='text-align: center; height: 300px; overflow: hidden;'>
                        <img src="{poster}" alt="{name}" style="width: 100%; height: auto; max-height: 180px;">
                        <h4 style='color: #FFFFFF; font-size: 14px; margin: 10px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{name}</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Add custom CSS for a cool UI
st.markdown(
    """
    <style>
    body {
        background-color: #f9f9f9; /* Light background for the app */
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff6347, #ff4500); /* Gradient button color */
        color: white; /* Button text color */
        border-radius: 10px; /* Rounded corners */
        height: 50px; /* Increased button height */
        font-size: 16px; /* Button text size */
        transition: background 0.3s, transform 0.3s; /* Smooth transition */
        border: none; /* Remove border */
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff4500, #ff6347); /* Reverse gradient on hover */
        transform: scale(1.05); /* Slightly enlarge button on hover */
    }
    h1, h2 {
        margin: 10px 0; /* Space around headings */
    }
    .stSelectbox {
        margin: 20px 0; /* Space below selectbox */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown("<footer style='text-align: center; margin-top: 50px;'><p style='color: #777;'>Created by Amit Kumar | Movie Recommender System © 2024</p></footer>", unsafe_allow_html=True)
