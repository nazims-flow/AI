import streamlit as st
import pickle
import pandas as pd

def recommend(musics):
    music_index = music[music['title'] == musics].index[0]
    distances = similarity[music_index]
    music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_music = []
    for i in music_list:
        recommended_music.append(music.iloc[i[0]].title)
    return recommended_music

music_dict = pickle.load(open(r'E:\AAI Practical\Music Reccomend System\music_rec_system\musicrec.pkl', 'rb'))
music = pd.DataFrame(music_dict)

similarity = pickle.load(open(r'E:\AAI Practical\Music Reccomend System\music_rec_system\similarities.pkl', 'rb'))

st.title('Music Recommendation System')

selected_music_name = st.selectbox('Select a music you like', music['title'].values)

if st.button('Recommend'):
    recommended_names = recommend(selected_music_name)

    for name in recommended_names:
        st.markdown(f"### {name}")
