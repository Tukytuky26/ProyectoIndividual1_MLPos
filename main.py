from fastapi import FastAPI
import pandas as pd
import pickle
import joblib

app = FastAPI()

#http://127.0.0.1:8000

@app.get('/')
def index():
     introduccion = {'introduction': 'Operaciones de Aprendizaje Automático (MLOps)',
                     'creadora': 'Melina Arroyo',
                     'github': 'https://github.com/Tukytuky26',
                     'LinkeIn': 'Melina Arroyo Cisneros'           
                    } 
     return introduccion


@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    data = pd.read_csv('_scr/data/movies_etl_fa.csv')
    idioma = idioma.lower()
    data['original_language'] = data['original_language'].str.lower()
    cantidad_peliculas = sum(data['original_language'] == idioma)
    peliculas_idioma = {'idioma': idioma,'cantidad': cantidad_peliculas}
    return peliculas_idioma

@app.get('/peliculas_duracion/{Pelicula}')
def pelicula_duracion(Pelicula:str):
    data = pd.read_csv('_scr/data/movies_etl_fa.csv')
    pelicula = data[data['title'].str.lower() == Pelicula.lower()]
    informacion_peliculas = []
    for i, row in pelicula.iterrows():
        pelicula_info = {
            'titulo': row['title'],
            'duracion': row['runtime'],
            'Año': row['release_year']
        }
        informacion_peliculas.append(pelicula_info)
    return informacion_peliculas

@app.get('/peliculas_franquicia/{Franquicia}')
def peliculas_franquicia(Franquicia:str):
    data = pd.read_csv('_scr/data/movies_etl_fa.csv')
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

@app.get('/peliculas_pais/{Pais}')
def peliculas_pais(Pais: str):
    data = pd.read_csv('_scr/data/movies_etl_fa.csv')  # Reemplaza con la ruta y nombre de tu archivo CSV
    pais = Pais.lower()  # Convertir el nombre del país a minúsculas
    data['production_countries'] = data['production_countries'].str.lower()  # Convertir la columna 'pais' a minúsculas
    cantidad_peliculas = data['production_countries'].apply(lambda x: pais in x).sum()
    peliculasxpais = {'pais': Pais, 'cantidad': int(cantidad_peliculas)}
    return peliculasxpais

@app.get('/productoras_exitosas/{Productora}')
def productoras_exitosas(Productora:str):
    data = pd.read_csv('_scr/data/movies_etl_fa.csv')
    productora = Productora.lower()
    data['production_companies'] = data['production_companies'].str.lower()  # Convertir las productoras de cada película a minúsculas
    peliculas_productora = data[data['production_companies'].apply(lambda x: productora in x)]  # Filtrar películas por productora
    ganancia_total = peliculas_productora['revenue'].sum()  # Calcular el revenue total
    cantidad_peliculas = peliculas_productora.shape[0]
    productora_exito = {'productora':Productora,'revenue_total':float(ganancia_total),'cantidad': int(cantidad_peliculas)}
    return productora_exito

@app.get('/get_director/{Director}')
def get_director(Director:str):
    data = pd.read_csv('_scr/data/movies_etl_fa.csv')   # Reemplaza con la ruta y nombre de tu archivo CSV
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
def recommend(titulo):
    muestra = pd.read_csv('_src/data/model_data.csv')
    data = joblib.load('_src/data/similarity.pkl')
    index = muestra[muestra['title'] == titulo].index[0]
    distances = data[index] 
    similar = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    similar_indice = [i for i, _ in similar[1:6]]
    similar_pelis = muestra['title'].iloc[similar_indice].values.tolist()
    return {'peliculas_recomendadas': similar_pelis}