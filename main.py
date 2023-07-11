#Se importan los módulos necesarios: FastAPI para crear la API, pandas para el manejo de datos en formato CSV, pickle y joblib para cargar archivos de modelo. Se crea una instancia de la aplicación FastAPI utilizando la variable app.
from fastapi import FastAPI
import pandas as pd
import pickle
import joblib


app = FastAPI()

#http://127.0.0.1:8000

#Se define un endpoint para la ruta raíz ("/"). Cuando se accede a esta ruta mediante una solicitud GET, se devuelve un diccionario con información de introducción sobre el proyecto.
@app.get('/')
def index():
     introduccion = {'introduction': 'Operaciones de Aprendizaje Automático (MLOps)',
                     'creadora': 'Melina Arroyo',
                     'github': 'https://github.com/Tukytuky26',
                     'LinkeIn': 'Melina Arroyo Cisneros'           
                    } 
     return introduccion


#Se define un endpoint para la ruta "/peliculas_idioma/{idioma}". Cuando se accede a esta ruta con un idioma específico, se carga un archivo CSV de películas, se convierte el idioma a minúsculas y se cuenta cuántas películas están en ese idioma. Se devuelve un diccionario con el idioma y la cantidad de películas.
@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    data = pd.read_csv('_src/data/movies_etl_fa.csv')
    idioma = idioma.lower()
    data['original_language'] = data['original_language'].str.lower()
    cantidad_peliculas = sum(data['original_language'] == idioma)
    peliculas_idioma = {'idioma': idioma,'cantidad': cantidad_peliculas}
    return peliculas_idioma

#Se define un endpoint para la ruta "/peliculas_duracion/{Pelicula}". Cuando se accede a esta ruta con el nombre de una película, se carga el archivo CSV de películas y se busca la información de duración y año de lanzamiento para la película especificada. Se devuelve una lista de diccionarios con la información de cada película encontrada.
@app.get('/peliculas_duracion/{Pelicula}')
def pelicula_duracion(Pelicula:str):
    data = pd.read_csv('_src/data/movies_etl_fa.csv')
    pelicula = data[data['title'].str.lower() == Pelicula.lower()] # Filtrar las películas por nombre de pelicula
    informacion_peliculas = []
    for i, row in pelicula.iterrows():
        pelicula_info = {
            'titulo': row['title'],
            'duracion': row['runtime'],
            'Año': row['release_year']
        }
        informacion_peliculas.append(pelicula_info)
    return informacion_peliculas

#Se define un endpoint para la ruta "/peliculas_franquicia/{Franquicia}". Cuando se accede a esta ruta con el nombre de una franquicia, se carga el archivo CSV de películas y se filtran las películas que pertenecen a esa franquicia. Se calcula la cantidad de películas, la ganancia total y el promedio de ganancia de la franquicia. Se devuelve un diccionario con esta información.
@app.get('/peliculas_franquicia/{Franquicia}')
def peliculas_franquicia(Franquicia:str):
    data = pd.read_csv('_src/data/movies_etl_fa.csv')
    data['belongs_to_collection'] = data['belongs_to_collection']
    franquicia = data[data['belongs_to_collection'].str.lower() == Franquicia.lower()]  # Filtrar las películas por nombre de franquicia
    cantidad_peliculas = franquicia['title'].count()  # Obtener la cantidad de películas
    ganancia_total = franquicia['revenue'].sum()  # Calcular la ganancia total
    promedio_ganancia = franquicia['revenue'].mean()  # Calcular el promedio de ganancia

    informacion_franquicia = {
        'franquicia': Franquicia,
        'cantidad': int(cantidad_peliculas),
        'ganancia_total': float(ganancia_total),
        'ganancia_promedio': promedio_ganancia
    }

    return informacion_franquicia

#Se define un endpoint para la ruta "/peliculas_pais/{Pais}". Cuando se accede a esta ruta con el nombre de un país, se carga el archivo CSV de películas y se cuenta cuántas películas fueron producidas en ese país. Se devuelve un diccionario con el nombre del país y la cantidad de películas.
@app.get('/peliculas_pais/{Pais}')
def peliculas_pais(Pais: str):
    data = pd.read_csv('_src/data/movies_etl_fa.csv')  # Reemplaza con la ruta y nombre de tu archivo CSV
    pais = Pais.lower()  # Convertir el nombre del país a minúsculas
    data['production_countries'] = data['production_countries'].str.lower()  # Convertir la columna 'pais' a minúsculas
    cantidad_peliculas = data['production_countries'].apply(lambda x: pais in x).sum()
    peliculasxpais = {'pais': Pais, 'cantidad': int(cantidad_peliculas)}
    return peliculasxpais

#Se define un endpoint para la ruta "/productoras_exitosas/{Productora}". Cuando se accede a esta ruta con el nombre de una productora, se carga el archivo CSV de películas y se filtran las películas producidas por esa productora. Se calcula la ganancia total y la cantidad de películas de esa productora. Se devuelve un diccionario con esta información.
@app.get('/productoras_exitosas/{Productora}')
def productoras_exitosas(Productora:str):
    data = pd.read_csv('_src/data/movies_etl_fa.csv')
    productora = Productora.lower()
    data['production_companies'] = data['production_companies'].str.lower()  # Convertir las productoras de cada película a minúsculas
    peliculas_productora = data[data['production_companies'].apply(lambda x: productora in x)]  # Filtrar películas por productora
    ganancia_total = peliculas_productora['revenue'].sum()  # Calcular el revenue total
    cantidad_peliculas = peliculas_productora.shape[0]
    productora_exito = {'productora':Productora,'revenue_total':float(ganancia_total),'cantidad': int(cantidad_peliculas)}
    return productora_exito

@app.get('/get_director/{Director}')
def get_director(Director:str):
    data = pd.read_csv('_src/data/movies_etl_fa.csv')   # Reemplaza con la ruta y nombre de tu archivo CSV
    director = Director.lower()
    data['director'] = data['director'].str.lower().fillna('')  # Convertir los nombres de los directores a minúsculas
    peliculas_director = data[data['director'].apply(lambda x: director in x)]
    retorno_total = peliculas_director['return'].sum()
    director = {'director': Director}
    retorno_total = {'retorno_total_director': retorno_total}

    informacion_peliculas = []
    for i, row in peliculas_director.iterrows():# Generar una lista de diccionarios con la información requerida para cada película
        pelicula_info = {
            'peliculas': row['title'],
            'anio': row['release_year'],
            'retorno_pelicula': row['return'],
            'budget_pelicula': row['budget'],
            'revenue_pelicula': row['revenue']
        }   
        informacion_peliculas.append(pelicula_info)
    return director, retorno_total, informacion_peliculas


@app.get('/recomendacion/{titulo}')
def recommend(titulo:str):
    muestra = pd.read_csv('_src/data/data_model.csv')
    data = joblib.load('_src/data/similarity.pkl') 
    index = muestra[muestra['title'] == titulo].index[0]
    distances = data[index] 
    similar = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])
    similar_indice = [i for i, _ in similar[1:6]]
    similar_pelis = muestra['title'].iloc[similar_indice].values.tolist()
    return {'titulo': str(titulo), 'recomendaciones':similar_pelis}
    