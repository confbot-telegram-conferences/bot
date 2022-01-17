Instalación
===========
El proyecto está configurado para ser utilizado sobre docker, lo que facilita el proceso de instalación y puesta en marcha el sistema.
Para comenzar de forma sencilla puede usar **vscode**, pues ya tiene la configuración de `.devcontainer`. 
Si no desea usar **vscode** puede ejecutar el proyecto directamente usando `docker-compose` y el fichero `local.yml`.
Haciendo una búsqueda simple en el código, podrá encontrár toda la configuración que se tiene de docker.

Variable de entornos
====================
- TELEGRAM_TOKEN= <Token del bot en telegram>
- MONGO_CONECTION=mongodb://mongodb:27017/
- MONGO_DATABASE=develoment_database <Nombre de la base de datos en mongodb>
- APP_KEY=<Generar una cadena aleatoria que servirá como key de la aplicación>
- BACKEND_URL=http://django:8000
- TELEGRAM_BOT_NAME=<Nombre del bot de telegram>

Estructura del proyecto
=======================
Para interactuar con telegram el sistema utiliza `python-telegram-boot`. 
Inicialmente se pretendía que el bot fuera capáz de interactuar con varias platformas de chat, pero con el tiempo esto fue poco productivo.
Es así que dentro de la carpeta **app** podrán ver dos carpetas, **handlers** y **handlers2**.
Donde en **handlers2** está el código nuevo que se comenzó a implementar en el sistema. El objetivo es eliminar en el futuro la carpeta **handlers**.

Internamente el bot utiliza una base de datos mongodb para guardar datos temporales, pero la datos fundamentales se guardan en el backend, que es otra aplicación.
Una de las variables de entornos que se debe configurar es **APP_KEY**. 
Este valor es utilizado para interactuar con el backend, que lo utiliza para validar las peticiones.

Deficiencias del proyecto
=========================
El sistema está formado por dos aplicaciones.
El bot, esta aplicación, que tiene como función interactuar con telegram.
Y el backend que es donde está la base de datos y la lógica del negocio.
Con el tiempo se vio que era más produtivo tener toda la lógica en una sola aplicación, es decir, esta aplicación puede ser eliminada en el futuro.
La idea sería pasar toda la lógica del bot para el backend y así tener solo una aplicación. Esto facilita las laborares de mantenimiento de la aplicación.