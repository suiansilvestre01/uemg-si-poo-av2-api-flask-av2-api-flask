# API de Controle Financeiro Pessoal (Flask + SQLite)

## Descrição
API REST simples em Flask para controle financeiro pessoal com autenticação JWT. Usuários podem cadastrar, fazer login e gerenciar suas transações (receitas/despesas). Cada usuário só vê suas próprias transações.

## Estrutura
- app.py
- database.py
- models/
  - user.py
  - registro.py
- routes/
  - users.py
  - registros.py
- requirements.txt

## Instalação
1. Clone o repositório
2. Crie um ambiente virtual e ative:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   venv\Scripts\activate   # Windows
   ```
3. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Rode a aplicação:
   ```bash
   python app.py
   ```
A API ficará disponível em `http://127.0.0.1:5000/`.

## Endpoints principais

### Registrar usuário
`POST /register`
```json
{
  "username": "joao",
  "email": "joao@email.com",
  "password": "12345"
}
```

### Login
`POST /login`
```json
{
  "email": "joao@email.com",
  "password": "12345"
}
```
Resposta:
```json
{
  "token": "SEU_JWT_AQUI"
}
```

### Criar transação (protegido)
`POST /transacoes`
Header:
```
Authorization: Bearer SEU_TOKEN
```
Body:
```json
{
  "valor": 120.5,
  "categoria": "Alimentação",
  "descricao": "Mercado",
  "data": "2025-11-25",
  "tipo": "despesa"
}
```

### Listar transações do usuário (protegido)
`GET /transacoes`
Header:
```
Authorization: Bearer SEU_TOKEN
```

### Consultar / Atualizar / Deletar por id
`GET /transacoes/<id>`
`PUT /transacoes/<id>`
`DELETE /transacoes/<id>`
(Todos protegidos - usam o token no header)

## Observações
- Troque a `SECRET_KEY` em produção.
- Banco SQLite `fin_api.db` será criado automaticamente no diretório do projeto.