Ejemplo para implementar un proyecto en flask


## Instrucciones para probar

* Clonar el repositorio de Github
* Ejecuta el siguiente comando para instalar los paquetes
    - pip install -r requirements.txt
* Copia el archivo *“.env.example”* y lo renombras de la siguiente forma *“.env”*
    - Dentro del archivo encontraras 2 keys que son las variables de entorno que necesita la aplicación
        - ENV: Especifica el ambiente donde se va a trabajar
            - Ambientes de desarrollo soportados
                - development
                - testing
                - production
        - SECRET_KEY: Debemos crear un string random para utilizarlo como complemento de la contraseña 
        - DATABASE_URL: Es la URL de la base de datos
            - Formato necesario para la conexión a la base de datos
                - mysql+pymysql://{usuario}:{password}@{host}/{nombre_de_base_de_datos}
    - En el archivo *“.env.example”* también se encuentran las credenciales necesarias para el contenedor de MySQL
* Ejecuta las migraciones del sistema con el siguiente comando
    - flask db upgrade
* Ejecutar el sistema con el siguiente comando
    - python wsgi.py
* Para corroborar que el sistema está en ejecución, utiliza el endpoint llamado  *“Test url”* , que se encuentra en la colección de Postman. Esta colección está disponible en la carpeta de utilidades del proyecto.



#### Tests
* Para ejecutar las pruebas, utiliza los siguientes comandos
    - python -m unittest *”(Ejecuta todos los test)”*
    - python -m unittest directory/test.py -k test_function *”(ejecuta un test especifico)”*
    - NOTA: **Cada vez que se ejecutan los test se elimina la base de datos**

* Para ejecutar el test coverage 
    - coverage run -m unittest discover
    - coverage report


#### Docker
* Si necesitas usar Docker, puedes levantar el proyecto de la siguiente manera
    1. Construye el proyecto *(Se debe ejecutar cada vez que hagas un cambio en archivo dockerfile o docker-compose.yaml)* 
        - docker compose -f docker-compose.yaml -f docker-compose.services.yaml build
    2. Levanta el proyecto en segundo plano
        - docker compose -f docker-compose.yaml -f docker-compose.services.yaml up -d 
    3. Para acceder al contenedor de la aplicación
        - docker exec -it backend-app /bin/bash
* Para eliminar el proyecto necesitas el siguiente comando
    1. docker compose -f docker-compose.yaml -f docker-compose.services.yaml down


## Desarrollado con

* Python
* Mysql



#### Librerias principales

* Flask
* SQLAlchemy
* Marshmallow
