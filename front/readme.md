# Gerenciador de Exames Médicos - Frontend
### Este é o frontend do projeto Gerenciador de Exames Médicos, uma aplicação web para gerenciar registros de pacientes e prever riscos cardíacos usando uma API REST. A interface permite listar, criar, editar, deletar e prever o risco cardíaco de pacientes.

## Estrutura do Projeto

- index.html: Página principal com o formulário e a tabela de pacientes.
- styles.css: Estilização da interface, incluindo responsividade com media queries.
- script.js: Lógica JavaScript para interagir com a API (listar pacientes, enviar formulários, realizar predições).

## Pré-requisitos

- Um navegador web moderno (Chrome, Firefox, etc.).
- A API do projeto deve estar rodando em http://localhost:5000 (veja o README da API em ../api/).

## Como Usar

- Use um servidor local, como o Live Server no VS Code, ou abra o index.html diretamente no navegador (algumas funcionalidades podem ser limitadas devido a CORS).
- Certifique-se de que a API está rodando
- A tabela exibirá todos os pacientes cadastrados na API.


##Funcionalidades:

- Listar pacientes: A tabela mostra todos os pacientes com colunas como ID, idade, sexo, etc.
- Adicionar paciente: Preencha o formulário e clique em "Cadastrar".
- Editar paciente: Clique em "Editar" na tabela, preencha o formulário e envie.
- Deletar paciente: Clique em "Deletar" na tabela.
- Prever risco cardíaco: Clique em "Prever" para calcular o risco (0 = sem risco, 1 = com risco) usando o modelo de machine learning.


## Configuração do Ambiente

- Dependências: Nenhuma dependência externa é necessária, pois o frontend usa apenas HTML, CSS e JavaScript puro.
- Responsividade: O CSS inclui media queries para telas menores (ex.: tablets e celulares), ajustando o layout da tabela e formulário.


## Resolução de Problemas

- Erro de CORS: Verifique se a API está rodando e se o CORS(app) está configurado em app.py.
- Tabela vazia: Confirme que a API está retornando dados em http://localhost:5000/api/patients.
- Mensagens de erro em inglês: Certifique-se de que o backend retorna mensagens em português (definidas em schema.py).
