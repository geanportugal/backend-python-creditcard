# backend-python-creditcard
Desafio para vaga de backend na MaisTodos

![portaldetodos](https://avatars0.githubusercontent.com/u/56608703?s=400&u=ae31a7a07d28895589b42ed0fcfc102c3d5bccff&v=4)

Desafio técnico `Python`
========================

## Técnologias utilizadas
  - Python
  - Django
  - Django Rest Framework
  - Postgres
  - Docker

Instalando o Projeto
-----------------

  - Use Docker!!! - Download  [here](https://www.docker.com/get-started);
  - Faça o clone do projeto em sua máquina local, use git clone;

Iniciando o Projeto
-----------------
  - Execute o docker
  - vá até a pasta **dotenv** e renomeie o arquivo **.env_example** para **.env**
  - Agora configure as variaveis de ambiente
  - para gerar o Secret_key use python 3.6 ou superior, no console digite python ou python3 e execute os comandos 
  ```python
     import secrets
     print(secrets.token_urlsafe(64))
  ```
  - Copie o conteudo e substitua na variavel de ambiente **SECRET_KEY**
  - agora gere o token para encriptar o cartão de crédito
  ```python
     import secrets
     print(secrets.token_urlsafe(32))
  ```
  - Copie o conteudo e substitua na variavel de ambiente **SECRET_KEY_CARD**
  - Em seguida gere o salt, também usado na criptografia do cartão
  ```python
     import secrets
     print(secrets.token_urlsafe(16))
  ```
  - Copie o conteudo e substitua na variavel de ambiente **SALT**
  - agora de um nome ao banco de dados, usuário e senha e porta de conexão do postgres, substituindo as variaveis de ambiente **POSTGRES_DB**, **POSTGRES_USER**, **POSTGRES_PASSWORD**, **POSTGRES_PORT** - a porta padrão é a 5432, o host não altere, pois estamos usando o o network em modo bridge
  - substitua as variaveis de ambiente **SUPERUSER_USERNAME**, **SUPERUSER_EMAIL**, **SUPERUSER_PASSWORD**, com os dados do seu usuário para acesso ao django admin e também sera usado para gerar o token da api

Feito tudo isso agora vamos executar o projeto finalmente, pela linha de comando vá até a pasta raiz do projeto e execute o seguinte comando 
```shell
  docker-compose up --build
```
Este comando ira executar os seguintes passos

- Download das imagens necessárias
- Criara os containers do arquivo docker-compose.yml
- criara o banco de dados
- ira executar as migrações do projeto
- ira criar um super usuario do django
- executara os testes unitários e de integração
- rodara o runserver do Django na porta 8000

Se tudo correu bem acesse a api pelo endereço http://localhost:8000

## Acessando os endpoints da API
```shell
  GET  /api/v1/credit-card - listar os cartões de crédito
  GET  /api/v1/credit-card/`<key>` - detalhe do cartão de crédito
  POST /api/v1/credit-card/ - cadastrar um novo cartão de crédito
  GET  /api/v1/docs - acessa a documentação - swagger
  GET  /api/v1/redoc - acessa a documentação - Redoc
  POST  /api/v1/token/- Endpoint para gerar o token de autorização
  POST  api/v1/token/refresh/ - Endpoint para refrescar o token
```


  
Gerando o Token
--------
Sera gerado um token do tipo JWT Bearer
```shell
    POST  /api/v1/token/
    {
        "username": "maistodos",
        "password": "maistodos"
    }

```
Utilizando o Token
--------
```shell
curl --location '/api/v1/credit-card/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwNDIxNTI1LCJpYXQiOjE2OTA0MTc5MjUsImp0aSI6IjQ1NGJkNzdhMzEwODQ5NzFiYWUxZTFmYjY4MGJmODY1IiwidXNlcl9pZCI6MX0.3NvBRwwc6FGfekeP0luqBtcV25LHBIOpt4VLxihMRGA' \
--header 'Content-Type: application/json' \
--data ' {
        "number": "5591972411369972",
        "exp_date": "02/2026",
        "holder": "John Doe",
        "cvv": "123"
    }'
```
* **Importante:** Para todas as chamadas da api será necessário utilizar o token

![Luck](https://media.giphy.com/media/l49JHz7kJvl6MCj3G/giphy.gif)

