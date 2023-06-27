import streamlit as st
import pandas as pd
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

key_dict = json.loads(st.secrets["textkey"])
creds = credentials.Certificate(key_dict)
if not firebase_admin._apps:
    firebase_admin.initialize_app(creds)

db = firestore.client()
dbmovies = db.collection(u"movies")

st.title("Netflix App")
sidebar = st.sidebar
today = datetime.date.today()
sidebar.success('Current date: %s' % today)

@st.cache_data
def load_data():
    collection_ref = dbmovies
    query = collection_ref.stream()
    data = []
    for doc in query:
        data.append(doc.to_dict())
    return data

data = load_data()

show_all = sidebar.checkbox("Mostrar todos los filmes")
if show_all:
    st.dataframe(pd.DataFrame(data))

def loadByTitulo(titulo):
    movies_ref = dbmovies.where(u'name', u'==', titulo)
    currentMovie = None
    for myMovie in movies_ref.stream():
        currentMovie = myMovie
    return currentMovie

#st.sidebar.subheader("Titulo del Filme")
tituloSearch = st.sidebar.text_input("Titulo del Filme")
btnFiltrar = st.sidebar.button("Buscar filmes")

if btnFiltrar:
    doc = loadByTitulo(tituloSearch)
    if doc is None:
        st.sidebar.write("Filme no existe")
    else:
        st.sidebar.write(doc.to_dict())

#data = load_data()
directors = [record['director'] for record in data]
selected_director = sidebar.selectbox('Seleccionar Director:', directors)

def filter_films_by_director(director):
    filtered_films = [record for record in data if record['director'] == director]
    return filtered_films

search_button = sidebar.button('Filtrar Director')

if search_button:
    if selected_director:
        st.markdown("_____")
        st.write(f"Filmes del director {selected_director}")
        filtered_films = filter_films_by_director(selected_director)
        st.dataframe(pd.DataFrame(filtered_films))
    else:
        st.write('Please select a director')
