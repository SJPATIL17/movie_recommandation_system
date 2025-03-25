import pickle
import streamlit as st
import requests

# TMDb API Key (Replace with your valid API Key)
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"


# Function to fetch the movie poster from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            return "https://via.placeholder.com/150?text=No+Image"  # Placeholder if no image found
    except:
        return "https://via.placeholder.com/150?text=Error"


# Function to get recommended movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    google_search_links = []

    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        movie_name = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_id)
        google_search_url = f"https://www.google.com/search?q={movie_name.replace(' ', '+')}+movie"

        recommended_movie_names.append(movie_name)
        recommended_movie_posters.append(poster_url)
        google_search_links.append(google_search_url)

    return recommended_movie_names, recommended_movie_posters, google_search_links


# Streamlit UI
st.header('🎬 Movie Recommender System')

# Load movie data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a movie:", movie_list)

# Show recommendations
if st.button('🔍 Show Recommendations'):
    recommended_movie_names, recommended_movie_posters, google_search_links = recommend(selected_movie)

    st.write("### Recommended Movies:")

    col1, col2, col3, col4, col5 = st.columns(5)  # Create 5 columns for displaying movies

    columns = [col1, col2, col3, col4, col5]

    for i in range(5):
        with columns[i]:
            st.image(recommended_movie_posters[i], width=150)  # Display movie poster
            st.markdown(f"[🎥 {recommended_movie_names[i]}]( {google_search_links[i]} )",
                        unsafe_allow_html=True)  # Clickable link
