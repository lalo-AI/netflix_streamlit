import streamlit as st
import pandas as pd
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# El código configura las credenciales de Firebase, inicializa la aplicación de Firebase 
# si aún no se ha inicializado, crea un cliente de Firestore y recupera una referencia a la colección 
# de "movies" en Firestore mediante la variable dbmovies. Esto le permite interactuar con 
# la base de datos de Firestore y realizar operaciones en la colección de "movies".

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
data = load_data()

show_all = sidebar.checkbox("Mostrar todos los filmes")
if show_all:
    st.dataframe(pd.DataFrame(data))
    st.markdown("_____")

# Se define la función que retorma el segmento del dataframe generado para los filmes
# que contengan la palabra o letras a buscar
def search_title(tituloSearch):
    search_input_lower = tituloSearch.lower()
    if tituloSearch:
        # Con esto línea de código se asegura la busqueda del flime las cuales estén contenidas en la
        # variable sin importar que sean minúsculas o mayúsculas
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

# Código para iniciar la busqueda del film
tituloSearch = st.sidebar.text_input("Titulo del Filme")
search_button = st.sidebar.button('Buscar filmes')
if search_button:
    search_title(tituloSearch)

#...
# Código para iniciar la busqueda de Director y muestre en pantalla
# los filmes que tiene asociados
directors = [record['director'] for record in data]
selected_director = sidebar.selectbox('Seleccionar Director:', directors)

def filter_films_by_director(director):
    filtered_films = [record for record in data if record['director'] == director]
    return filtered_films

search_button = sidebar.button('Filtrar Director')

if search_button:
    if selected_director:
        filtered_films = filter_films_by_director(selected_director)
        num_films = len(filtered_films)
        st.write(f"Total filmes : {num_films} Director : {selected_director}")
        st.dataframe(pd.DataFrame(filtered_films))
    else:
        st.write('Please select a director')

#...
# Código para insertar un nuevo filme, en este caso estoy utilizando selectbox en
# los campos que de cierta manera no quisiera dejar en blanco si no que de la misma
# BD el usuario seleccione la compañía, el director y el genero dejando solo abierto
# el nombre de la pelicula

st.markdown("_____")
st.header("Nuevo Filme")

name = sidebar.text_input("Name")
companies = [record['company'] for record in data]
selected_company = sidebar.selectbox('Company', companies)
directors = [record['director'] for record in data]
selected_director = sidebar.selectbox('Director', directors)
genre = [record['genre'] for record in data]
selected_genre = sidebar.selectbox('Genre', genre)
submit = sidebar.button("Crear nuevo filme")

# Una vez que el nombre se ha enviado se carga la información en la BD
new_filme = False
if name and companies and directors and genre and submit:
  doc_ref = db.collection("movies").document()
  doc_ref.set ({
      "name": name,
      "company": selected_company,
      "director": selected_director,
      "genre": selected_genre
  })
  st.sidebar.write("Filme insertado correctamente")
  new_filme = True

# Fetch the last added document
if new_filme:
  last_doc = doc_ref.get()
  if last_doc.exists:
    last_record = last_doc.to_dict()
    st.write("Último filme agregado:")
    st.write(pd.DataFrame([last_record]))
  else:
    st.write("Error: El último filme no se encuntra")

# El código recupera todos los documentos de la colección de "movies" en Firestore, 
# los convierte en diccionarios y luego crea un DataFrame usando los diccionarios 
# y un orden de columna específico. 
movies_ref = list(db.collection(u'movies').stream())
movies_dict = list(map(lambda x: x.to_dict(), movies_ref))
column_order = ["name","company", "director", "genre"]
movies_dataframe = pd.DataFrame(movies_dict, columns=column_order)

st.dataframe(movies_dataframe)
