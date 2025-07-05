# Como Executar
Opção 1: Com Docker (Recomendado)
1. Certifique-se de que o Docker e o Docker Compose estão instalados.
2. No diretório raiz do projeto (onde está o docker-compose.yml), execute:
docker-compose up --build
3. Acesse a API em http://localhost:5000 (redireciona para Swagger).
4. Para parar:
docker-compose down

Opção 2: Localmente
1. Clone o repositório e entre no diretório backend/:
cd backend
2. Crie um ambiente virtual:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
3. Instale as dependências:
pip install -r requirements.txt
4. Execute a API:
python app.py

Execução API
Para executar a API basta executar no diretório raiz:

flask run --host 0.0.0.0 --port 5000
Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.

flask run --host 0.0.0.0 --port 5000 --reload



5. Acesse a API em http://localhost:5000/apidocs (redireciona para Swagger).

# Endpoints da API
A API oferece os seguintes endpoints:

- GET /currencies
  - Retorna a lista de moedas na watchlist.
  - Resposta: Array de moedas ou {"message": "Nenhuma moeda na lista"}.
  - Exemplo: [{"code": "USD", "name": "Dólar Americano", "rate": 5.5, "updated_at": "2025-04-12T00:00:00"}]
- POST /currencies
  - Adiciona uma nova moeda.
  - Corpo: {"code": "USD", "name": "Dólar Americano", "rate": null}
  - Resposta: Moeda adicionada ou erro (400, 409).
  - Restrição: Apenas códigos permitidos (ex.: USD, EUR, BTC).
- PUT /currencies/<code>
  - Atualiza a taxa de uma moeda.
  - Corpo: {"rate": 5.6}
  - Resposta: Moeda atualizada ou erro 404.
- DELETE /currencies/<code>
  - Remove uma moeda.
  - Resposta: {"message": "Moeda removida"} ou erro 404.
Explore todos os endpoints em http://localhost:5000/swagger.

# Integração com o Frontend
- O frontend (rodando em http://localhost:8080) consome esta API para gerenciar a watchlist e atualizar taxas.
- Certifique-se de que a API está rodando antes de iniciar o frontend.
- A API suporta CORS, permitindo requisições do frontend.

# Banco de Dados
- Usa SQLite (watchlist.db) para armazenar moedas.

# Desenvolvimento
- Para adicionar novas moedas permitidas, edite ALLOWED_CURRENCIES em app.py.
- Para modificar endpoints, edite as classes CurrencyList e CurrencyResource em app.py.
- Para atualizar a documentação, modifique swagger_config em app.py e rebuild o projeto.
- Use o Swagger (/swagger) para testar endpoints durante o desenvolvimento.

# Problemas Comuns
- Erro 500 no banco: Verifique se watchlist.db tem permissões de escrita no diretório backend/.
- CORS bloqueado: Confirme que o frontend está acessando http://127.0.0.1:5000.
- Swagger não carrega: Certifique-se de que static/swagger.json foi gerado corretamente.
- Taxas não persistem: Verifique se as chamadas PUT estão atualizando rate e updated_at no banco.