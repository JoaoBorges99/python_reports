# API de Geração de Relatórios Excel

## Visão Geral

Esta API permite gerar relatórios em formato Excel a partir de consultas SQL em banco Oracle. Os endpoints possibilitam consultar dados, gerar arquivos Excel e registrar logs de erro.

---

## Endpoints

### 1. `GET /`

Retorna informações básicas sobre a API.

**Resposta:**
```json
{
  "version": "1.0.0",
  "message": "API geração de relatorios Excel",
  "status": true
}
```

---

### 2. `POST /gerador_relatorio/{file_name}`

Executa uma consulta SQL definida em um arquivo e retorna os dados para geração de relatório.

**Parâmetros:**
- `file_name` (path): Nome do arquivo SQL (sem extensão).
- `body` (json):
  - `filtros`: Filtros para consulta SQL (exemplo: `{"CODFILIAL": 1}`).
  - `extension`: Extensão do arquivo desejado (`xlsx` por padrão).

**Exemplo de requisição:**
```json
{
  "filtros": {"CODFILIAL": 1},
  "extension": "xlsx"
}
```

**Resposta de sucesso:**
```json
{
  "name": "produtos-1",
  "extension": "xlsx",
  "time": "02/09/2025 14:00:00",
  "message": "Relatorio gerado com sucesso",
  "error": false,
  "filtros": {"CODFILIAL": 1},
  "colunas": [...],
  "data": [...]
}
```

**Resposta de erro:**
```json
{
  "name": "produtos-1",
  "extension": "xlsx",
  "time": "02/09/2025 14:00:00",
  "message": "Erro ao gerar relatorio, erro: <detalhes>",
  "error": true,
  "filtros": {"CODFILIAL": 1},
  "colunas": [],
  "data": []
}
```

---

### 3. `POST /criando_excel/{file_name}`

Gera e salva um arquivo Excel com base nos dados retornados pelo endpoint anterior.

**Parâmetros:**
- `file_name` (path): Nome do arquivo SQL (sem extensão).
- `body` (json): Mesmo formato do endpoint `/gerador_relatorio/{file_name}`.

**Exemplo de requisição:**
```json
{
  "filtros": {"CODFILIAL": 1},
  "extension": "xlsx"
}
```

**Resposta:**  
Retorna o mesmo JSON do endpoint `/gerador_relatorio/{file_name}`.

---

### 4. `GET /favicon.ico`

Retorna o favicon da aplicação.

---

## Estrutura de Pastas

- **sql/**: Arquivos SQL utilizados nas consultas.
- **arquivos-gerados/**: Relatórios Excel gerados.
- **log/error/**: Logs de erro.

---

## Observações

- A documentação interativa está disponível em `/docs` (Swagger UI) e `/redoc` (ReDoc).
- Os arquivos SQL devem estar na pasta `sql/`.
- Os arquivos Excel gerados são salvos em `arquivos-gerados/`.
- Logs de erro são gravados em `log/error/`.

---

## Autores

- Equipe Python Reports

---