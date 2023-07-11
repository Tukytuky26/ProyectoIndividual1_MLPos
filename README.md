# **Modelo de Recomendación MLOps**

![image](_src/images/cine.png)

# **Introducción**

# **Planteamiento del problema**
En este proyecto se desea llevar a cabo un modelo de recomendación, donde se emplearán desde el tratamiento y la recolección de datos, hasta el entrenamiento y mantenimiento de Machine Learning, de manera que pueda haber nuevos datos.
El rol asignado es realizar un trabajo  como data scientist en una star-up que provee servicios de agregación de plataformas de streaming. En el cual, se debe crear un modelo de Machine learning que servirá como alternativa de recomendación de películas.
En la recolección de nuestros datos se tienen algunas deficiencias, debido a que la madurez de los mismos es poca, existen: datos anidados, in transformar, no hay procesos automatizados para la actualización de nuevas películas o series.

# **Objetivos**

* Desarrollar una API por medio de FastAPI, y posteriormente, realizar un deploymennt a traves de render para consumir la API.
* Desarrollar un modelo de recomendación de películas por medio de Machine learning

# **Herramientas utilizadas**
* Herramientas
* Python
* Fast api
* Uvicorn
* Render


# **Metodología **
# Etl: 
Se transformaron algunos datos  los cuales fueron:  
1. Se desanidaron los datos de las columnas que tenían como datos un diccionario o una lista, extrayendo solo la información que iba a utilizarse.
2. Se rellenaron los valores nulos de los campos de las columnas revenue y budget.
3. Se eliminaron los valores nulos de la variable release_date.
4. Se cambió a formato AAAA-mm-dd la columna release_date. Además, se creó la columna release_year, donde se extrajo el año de la fecha estreno.
5. Se creó la columna con el retorno de inversión, llamada return,  dividiendo dos columnas ( revenue/ budget) .
6. Se eliminaron las columnas que no se utilizaron: 

# Eda
Se buscó la relación que había entre las variables de las bases de datos, se realizó... columnas eliminadas un análisis para las variables numéricas, y otro, para las variables categóricas:
Variables numéricas 
1. Se realizo un análisis de correlación a través de una matriz de correlación.
2. Se analizaron los outliers por medio de un histograma y un diagrama de dispersión, de cada variable numérica.

Variables categóricas: 
1. se realizó un proceso de para la recomendación del sistema usando cosine_similarity

# APIs y Deployment 
Para este proceso se utilizaron las herramientas de fast api y Render. Primero, se realizaron las funciones que iba a ser utilizadas para hacer nuestras consultas, asi como nuestra función del modelo de recomendación, las cuales fueron las siguientes:
Def peliculas_idioma: Se ingresa un Idioma, devolviendo la cantidad de películas producidas en ese idioma

* def peliculas_duracion: Se ingresa una película, devolviendo la duración  y el año

* def franquicia: Se ingresa la franquicia , retornando la cantidad de películas, ganancia total y promedio.

* def películas_pais: Se ingresa un país, retornando la cantidad de películas producidas en el mismo.

* def productoras_exitosas: Se ingresa la productora, entregandote el revunue total y la cantidad de peliculas que realizo.

* def get_director: Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista.

* def recomendacion: Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

