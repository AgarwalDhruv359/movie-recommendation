

import streamlit as st
import pandas as pd
import pickle
import os

# ===== Function: Download similarity.pkl from Google Drive =====
def download_file_from_gdrive(file_id, destination):
    import gdown
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, destination, quiet=False)

# ===== Load movie_dict.pkl (must be in your repo) =====
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# ===== Check & Download similarity.pkl if not present =====
SIMILARITY_FILE = "similarity.pkl"
DRIVE_FILE_ID = "1DzDzAWJDC6X9Us88ToHJ4LyrhslA9T2W"  # Your Google Drive file ID

if not os.path.exists(SIMILARITY_FILE):
    with st.spinner("Downloading similarity matrix (first time only)..."):
        download_file_from_gdrive(DRIVE_FILE_ID, SIMILARITY_FILE)

# ===== Load similarity matrix =====
similarity = pickle.load(open(SIMILARITY_FILE, "rb"))

# ===== Recommender Function =====
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
    return [movies.iloc[i[0]].title for i in movies_list]

# ===== Streamlit UI =====
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Select a movie you like:", movies["title"].values)

if st.button("Recommend"):
    st.subheader("Top Recommendations:")
    for m in recommend(selected_movie):
        st.write("👉", m)
