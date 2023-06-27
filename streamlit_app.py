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

def search_title(tituloSearch):
    search_input_lower = tituloSearch.lower()
    if tituloSearch:
        st.markdown("_____")
        filtered_data = [record for record in data if search_input_lower in record['name'].lower()]
        if filtered_data:
            num_records = len(filtered_data)
            st.write(f"Total filmes mostrados: {num_records}")
            df = pd.DataFrame(filtered_data)
            st.write(df)
        else:
            st.write("No titles found.")
    else:
        st.write("Please enter a search title.")

# Button for searching
tituloSearch = st.sidebar.text_input("Titulo del Filme")
search_button = st.sidebar.button('Buscar filmes')

# Call the search_title function when the button is clicked
if search_button:
    search_title(tituloSearch)

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
        filtered_films = filter_films_by_director(selected_director)
        num_films = len(filtered_films)
        st.write(f"Total filmes : {num_films} de : {selected_director}")
        st.dataframe(pd.DataFrame(filtered_films))
    else:
        st.write('Please select a director')
