# Gerenciador de Exames Médicos - API
### A API fornece endpoints para criar, listar, atualizar, deletar pacientes e calcular o risco cardíaco de um paciente específico usando um modelo de machine learning otimizado. A documentação interativa está disponível via Swagger UI, e a API é testada com pytest para garantir robustez.

## Tecnologias Utilizadas
#### Python 3.12.10: Linguagem principal para o backend e treinamento do modelo.
#### Flask 3.1.1: Framework web para construir a API RESTful.
#### Flask-RESTful: Extensão para criar endpoints REST.
#### Flask-SQLAlchemy: ORM para gerenciar o banco de dados SQLite.
#### Flask-CORS: Suporte a requisições cross-origin (CORS) para integração com o frontend.
#### Flasgger: Geração de documentação interativa com Swagger/OpenAPI 3.0.3.
#### scikit-learn 1.6.1: Biblioteca para treinamento e predição do modelo de machine learning.
#### pandas: Manipulação de dados para o modelo e predições.
#### numpy: Suporte a cálculos numéricos.
#### matplotlib: Visualização de resultados do treinamento (boxplots).
#### pytest 8.4.1: Framework para testes automatizados.
#### SQLite: Banco de dados leve para armazenar registros de pacientes.
#### pickle: Serialização do modelo de machine learning (BEST_model.pkl).

## Estrutura do Projeto

#### app.py: Arquivo principal da API Flask, com endpoints para gerenciar pacientes e predições.
#### swagger.json: Documentação da API no formato OpenAPI 3.0.3, integrada com Flasgger.
#### model/model.py: Define o modelo SQLAlchemy para a tabela Patient.
#### schema/schema.py: Validações dos dados de entrada usando marshmallow.
#### tests/test_api.py: Testes automatizados com pytest.
#### tests/test_model.py: Testes automatizados com pytest.
#### BEST_model.pkl: Modelo treinado exportado utilizando o notebook do google colab


## Pré-requisitos
#### Python 3.12.10
#### Dependências listadas em requirements.txt
#### Recomendado o uso de um abiente virtual 

## Endpoints

#### GET /api/patients: Retorna todos os pacientes cadastrados.
#### POST /api/patients: Cria um novo paciente.
#### GET /api/patients/: Busca um paciente por ID.
#### PUT /api/patients/: Atualiza um paciente (redefine heart_disease para null).
#### DELETE /api/patients/: Deleta um paciente.
#### POST /api/patients//predict: Calcula o risco cardíaco usando BEST_model.pkl.

## Configuração do Ambiente

#### Banco de Dados: SQLite (database.db) é criado automaticamente na primeira execução.
#### Modelo de Machine Learning treinado com o dataset UCI Heart Disease.
#### Usa scikit-learn==1.6.1 para evitar erros de compatibilidade com o google colab.
#### Salvo como BEST_model.pkl no diretório da API.
