import streamlit as st
import pandas as pd
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

key_dict = json.loads(st.secrets["textkey"])
creds = credentials.Certificate (key_dict)
# Con esta verificación nos aseguramos que no este abierta otra app para inicializar
if not firebase_admin._apps:
    firebase_admin.initialize_app(creds)

# Se inicializa Firestore
db = firestore.client()
dbmovies = db.collection(u"movies")

# Comienza el código requerido en el reto
st.title("Netflix App")

# Creamos uns sección del lado derecho que se denomina barra lateral o sidebar
sidebar = st.sidebar

# Como plus vamos a mostrar la fecha actual al usuario
today = datetime.date.today()
sidebar.success('Current date: ''%s' % (today))

@st.cache_data
def load_data():
    # Query Firestore for all records
    collection_ref = dbmovies
    query = collection_ref.stream()
    # Create an empty list to store the retrieved records
    data = []
    # Iterate over the Firestore query results and add them to the data list
    for doc in query:
        data.append(doc.to_dict())
    return data

# Load the data from Firestore
data = load_data()

# Display checkbox for showing all records
show_all = sidebar.checkbox("Mostrar todos los filmes")

# Display the records based on the checkbox selection
if show_all:
    for record in data:
        st.write(record)

# ...
def loadByTitulo (titulo):
  movies_ref = dbmovies.where(u'nane', u'==', titulo)
  currentMovie = None
  for myMovie in movies_ref.stream():
    currentMovie = myMovie
  return currentMovie

st.sidebar.subheader("Titulo del Filme")
tituloSearch = st.sidebar.text_input("titulo")
btnFiltrar = st.sidebar.button("Buscar filmes")

if btnFiltrar:
    doc = loadByTitulo(tituloSearch)
    if doc is None:
        st.sidebar.write("Filme no existe")
    else:
        st.sidebar.write(doc.to_dict())

#sidebar.title('Search Films by Director')

# ...
# Selectbox for director
selected_director = sidebar.selectbox('Seleeccionar Director:', data['director'].unique())

# Function to filter films by director
def filter_films_by_director(director):
    filtered_films = data[data['director'] == director]
    return filtered_films

# Command button
search_button = sidebar.button('Filtrar Director')

# Handling search button click event


if search_button:
    if selected_director:
        st.markdown("_____")
        st.write(f"Filmes del director {selected_director}")
        filtered_films = filter_films_by_director(selected_director)
        st.write(filtered_films)
    else:
        st.write('Please select a director')

