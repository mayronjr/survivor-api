# ZSSN (Rede Social de Sobrevivência Zumbi)

Criado com o objetivo de catalogar os sobreviventes do apocalipse zumbi e permitir o cambio de recursos entre humanos não infectados, assim como marcar quais sobreviventes foram infectados.    

# Requerimentos

* python 3.9.12
* django >=4.0.0 <4.1.0
* djangorestframework
* pyyaml
* requests
* django-cors-headers
* psycopg2
* django-environ
* postgresql

# Inicializando o Projeto

## Iniciando um ambiente virtual

Para isso, abra a pasta do projeto e execute:

        python -m venv env
        source env/bin/activate

No Windows, execute:

        python -m venv env
        env/bin/activate

## Instalando dependencias

Após iniciar o ambiente virtual, execute na pasta do projeto:

        pip install -r req.txt

## Configurando o banco de dados

Essa API faz uso do banco de dados postgreSQL.

Como usamos variaveis de ambiante, crie um arquivo ````.env```` na pasta ```backend/cfehome/``` e configure ele seguindo o padrão do arquivo ````.env-model````.

Para mais informações sobre esse Banco de Dados, acesse [o site do postgreSQL](https://www.postgresql.org/).

## Iniciando e testando a API

Agora que temos o ambiente virtual de python e as dependências instaladas, podemos executar a API ou testá-la.

Para executar a API temos o comando ```python backend\manage.py runserver```

Para executar os testes da API temos o comando ```???????```

# End Points

Existem 7 End points validos no projeto, sendo 3 do tipo GET, 2 do tipo POST e 2 do tipo PATCH.

- ```GET```
 
        /api/survivor/get-all
        /api/survivor/get/:id
        /api/reports

- ```POST```

        /api/survivor/add
        /api/survivor/relate-infection

- ```PATCH```

        /api/survivor/update-location/:id
        /api/trade

Os end points são melhores detalhados no seguinte link: [Postman | survivor-api](https://documenter.getpostman.com/view/14635829/Uyr5nJeA)
