import streamlit as st
import pandas as pd
import pickle
import requests

st.title('Movie Recommendation Engine')
moviedata = pickle.load(open('movie_dictionary.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(moviedata)

option = st.selectbox(
    'Select movie',
    (movies['title'].values)
)


def fetch_poster(movie_id):
    response = requests.get(url='https://api.themoviedb.org/3/movie/{}?api_key=2d37a798568166eefa63b283a60b6574'.format(movie_id))
    data = response.json()
    return  "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def Recommand(name):
    index = movies[movies['title'] == name].index[0]
    related = similarity[index]
    movies_related = sorted(list(enumerate(related)), reverse=True, key=lambda x: x[1])[1:21]

    tmp = [] # movie title
    tmp_poster = [] # movie poster path
    for i in movies_related:
        movie_id = movies.iloc[i[0]].id

        # also want to fetch the poster from api
        tmp.append(movies.iloc[i[0]]['title'])
        tmp_poster.append(fetch_poster(movie_id))
    return tmp, tmp_poster


if st.button('recommend'):
    recommendations, poster = Recommand(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    arr = [col1, col2, col3, col4, col5]

    cnt = -1
    for i in range(len(recommendations)):
        cnt = (cnt+1)%5
        with arr[cnt]:
            st.text(recommendations[i])
            st.image(poster[i])

