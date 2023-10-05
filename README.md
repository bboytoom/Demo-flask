# ChatBot Stock

Chatbot Stock es un aplicación web permite a los usuarios consultar los precios de multiples acciones utilizando un símbolo bursátil.


## Features

* Obtener el precio de las acciones del mercado de valores a través de una interfaz web
* Generar un historial de los precios consultados por el usuario
* Gráficos de la variación de los precios

### WIKI
[Documento de requerimientos](https://github.com/bboytoom/Chatbot-Stock/wiki/Documento-de-requerimientos)

[Documento de arquitectura](https://github.com/bboytoom/Chatbot-Stock/wiki/Documento-de-arquitectura)

[Colección de postman](https://github.com/bboytoom/Chatbot-Stock/blob/develop/utilities/ChatBot_Stock.postman_collection.json)


### Instrucciones para el Chatbot

* Clonar el repositorio de Github
* Ejecuta el siguiente comando para instalar los paquetes
    - pip install -r requirements.txt
* Copia el siguiente archivo *“.env.example”* y lo renombras de la siguiente forma *“.env”*
    - Dentro del documento hay 2 keys que son las variables de entorno
        - ENV: Especifica el ambiente donde se va a trabajar
            - Ambientes de desarrollo soportados por el sistema
                - development
                - testing
                - production
        - DATABASE_URL: Es la URL de la base de datos
            - Formato necesario para la conexión a la base de datos
                - mysql+pymysql://{usuario}:{password}@{host}/{nombre_de_base_de_datos}
* Ejecuta las migraciones del sistema con el siguiente comando
    - flask db upgrade
* Ejecutar el sistema con el siguiente comando
    - python wsgi.py
* Para corroborar que el sistema esta ejecución existe un endpoint llamado *“Test url”* que se encuentra en la colección de postman
    - La colección de postman se encuentra en la carpeta de utilidades del proyecto


## Desarrollado con

* Python
* Mysql


### Librerias principales

* Flask
* SQLAlchemy
* Marshmallow

**Paquetes utilizados**

* [requirements.txt](https://github.com/bboytoom/Chatbot-Stock/blob/develop/requirements.txt)
