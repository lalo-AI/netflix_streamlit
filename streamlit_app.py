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

data_load_state = st.text("Done! using (st.cache_data)")
st.markdown("_____")
data = load_data()

show_all = sidebar.checkbox("Mostrar todos los filmes")
if show_all:
    st.dataframe(pd.DataFrame(data))


btnFiltrar = st.sidebar.button("Buscar filmes")

def search_title(tituloSearch):
    # search_input = sidebar.text_input('Search title:')
    search_input_lower = tituloSearch.lower()
    if tituloSearch:
        st.markdown("_____")
        filtered_data = [record for record in data if search_input_lower in record['name'].lower()]
        if filtered_data:
            st.write("This is the information about the title(s):")
            df = pd.DataFrame(filtered_data)
            st.write(df)
        else:
            st.write("No titles found.")
    else:
        st.write("Please enter a search title.")

# Button for searching
tituloSearch = sidebar.text_input("Titulo del Filme")
#tit_lower = tituloSearch.lower()
search_button = sidebar.button('Buscar filmes')

# Call the search_title function when the button is clicked
if search_button:
    search_title(tituloSearch)

#if btnFiltrar:
#    movies = search_title(tituloSearch)
#    if not movies:
#        st.sidebar.write("Filme no existe")
#    else:
#        df = pd.DataFrame(movies)
#        st.write(df)

#...

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
