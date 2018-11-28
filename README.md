# Expansión de consultas para la captura de mensajes en Twitter relacionados con las drogas

## Contenido del repositorio

### Carpetas

- CONTEOS: contiene la contabilización de los términos tanto en el corpus de dominio como el de referencia.
- CORPUS: en esta carpeta se pueden encontrar los corpus de dominio y de referencia utilizados, los cuales han sido generados a traves de la API de Twitter
- EVALUACIÓN: aquí aparecen los ficheros que contiene las capturas de tuits de los candidatos resultantes.
- RANKING: contiene los candidatos finales generados tras la reordenación mediante word embeddings.
- RELEVANCE: contiene los candidatos tras la aplicación de la medida relevance para extraer la terminología de un corpus.

### Ficheros

- cuentaOcurrencias.py: además de realizarse el filtrado morfosintáctico en este fichero, se realiza el conteo de cada término (1-grama, 2-gramas y 3-gramas) en cada corpus.
- filtrarSemillas.py: de las semillas iniciales extraídas mediante la API de Twitter, se filtran aquellas que solo tengan los términos que nos interesan (Ketamina, Marihuana, Éxtasis).
- limpiarTweets.py: mediante la API de Twitter se obtiene una gran cantidad de campos para cada tuit, por lo que hacemos una limpieza de aquellos que son irrelevantes, quedandonos solo con el texto y la fecha de publicación.
- relevance.py: incluye la medida relevance que pondera los términos para extraer la terminología de un determinado corpus.
- rerankingW2V.py: incluye la aplicación de las tecnicas de word embeddings mediante el uso de Word2Vec, donde se comparan los términos resultantes de la aplicación del relevance con los términos semilla para mejorar los resutados finales.
- searchTwitter.py: realiza la captura de tuits de acuerdo a los términos clave añadidos en la query.
- utiles.py: realiza el filtro de los bigramas y trigramas que contienen algún unigrama.

## Word Embeddings

En el siguiente enlace se puede obtener el modelo entranado necesario para la ejecución del "reranking.py", sin el cual no se podrá realizar la comparación con las semillas iniciales.
[Modelo entranado Word2Vec](https://mega.nz/#!6N1n0IjD!ZVFx_lOU5TZ9cW28pU2_ko33m_uOhMqwFxh9_B4hci4)
