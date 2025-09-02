# 📌 Etapa 1 – Geração de Dados em Planilhas (.xlsx)

Este documento descreve o planejamento da **primeira fase** do projeto de automação para o setor de compras: a geração de planilhas de dados (blocos de informação) que os usuários poderão consumir para montar relatórios manuais.

---

## 🎯 Objetivo

* Mapear os **dados necessários** e suas respectivas fontes (tabelas Oracle ou relatórios Winthor).
* Desenvolver consultas SQL para extrair os blocos de dados.
* Validar consistência e desempenho das consultas.
* Estruturar a exportação em arquivos **.xlsx** via API em **Python**.
* Preparar o ambiente de armazenamento dos arquivos para o setor de compras.

---

## 📂 Escopo dos Dados

### **Dados do Produto**

* Filial → (tabela `pcprodut`)
* Código / Descrição → (tabela `pcprodut`)
* Classe → (tabela `pcprodut`)
* Quantidade total venda 90 dias → **Relatório de vendas (322)**
* Média venda 90 dias → **Relatório de vendas (322)**
* % Participação / Curva ABC → **Relatório de vendas (322)**
* Fora de linha → (tabela `pcprodut`)
* Estoque disponível, bloqueado, reservado, avaria → (tabelas `pcest`, `pclote`)
* Última entrada, custo real, preço de compra → (tabela `pcmov`)
* Fornecedor, comprador, departamento, marca, seção, linha → (tabelas `pcfornec`, `pccompr`, `pcdepart`, `pcmarca`, `pcsecao`, `pclinha`)
* Data cadastro produto → (tabela `pcprodut`)
* % Comissão interna/externa → (tabela `pccomiss`)

---

### **Dados do Fornecedor**

* Comprador → (tabela `pcfornec`)
* Tratador por (campo observação) → (tabela `pcfornec`)
* Contas a pagar → **Relatório contas a pagar (717 / 8194)**

  * Data emissão
  * Data vencimento
  * Prazo médio pagamento
* Projeto de venda por fornecedor → **Relatórios analíticos / vendas**
* Margem comprador / margem fornecedor → **Relatórios analíticos**
* Meta de venda fornecedor → **Relatórios de meta (8300 / 8178 / 8357)**
* Lead time (pedido x faturamento, emissão x liberação, etc.) → **Relatórios de entrada (211 / 8300)**
* Saldo a receber fornecedor → **Relatório 8178**
* Saldo a aplicar fornecedor → **Relatório 8357**

---

### **Analytics (Consolidados)**

* Entrada por fornecedor últimos 12 meses → **Relatórios de entrada (8300)**
* Faturamento por fornecedor últimos 12 meses → **Relatórios de venda (322)**
* Lead time mensal → **Relatório 211 / pedidos em aberto**
* Projeto de venda anual / mensal → **Relatórios analíticos**

---

## 📅 Cronograma Detalhado

| Semana    | Atividade                                                                           | Entregável                                            |
| --------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **1ª**     | **Mapeamento dos dados e fontes** (tabelas x relatórios)                            | Documento técnico com dicionário de dados.            |
| **2ª** | **Desenvolvimento das queries Oracle**                                              | Conjunto inicial de queries para blocos de dados.     |
| **2ª**     | **Validação dos resultados** (comparação com relatórios Winthor)                    | Relatório de validação de consistência.               |
| **3ª**     | **Implementação da API Python** para exportação em `.xlsx`                          | API funcional com geração de planilhas.               |
| **4ª**     | **Configuração do ambiente de armazenamento** (servidor, permissões, versionamento) | Diretório seguro e acessível para o setor de compras. |
| **4ª**     | **Entrega piloto e ajustes finais**                                                 | Pacote final da Etapa 1.                              |

---

## ⚡ Pontos de Atenção

* O tempo de **tracert/análise das rotinas** será essencial para garantir que os blocos de dados extraídos sejam equivalentes aos relatórios Winthor.
* Performance das queries deve ser otimizada para grandes volumes de dados.
* Divergências entre resultados SQL e relatórios devem ser ajustadas em conjunto com o setor de compras.

---

## ✅ Entregáveis da Etapa 1

* Dicionário de dados (o que buscar e onde buscar).
* Queries validadas no Oracle.
* API Python para exportação em `.xlsx`.
* Ambiente configurado para consumo dos arquivos.

---

## 📌 Etapa 2 – Automação da Geração de Planilhas

### 🎯 Objetivo

Automatizar a geração das planilhas finais atualmente produzidas manualmente pelo setor de compras, eliminando a necessidade de manipulação dos blocos de dados.

### 📂 Escopo

* Transformar queries e blocos de dados em **rotinas automatizadas** que consolidam as informações em um único arquivo final.
* Implementar **regras de negócio** que hoje são aplicadas manualmente (filtros, fórmulas, agrupamentos).
* Agendar a execução via **jobs** (ex.: cron, scheduler interno).

### ✅ Entregáveis

* Script/API para geração automática da planilha consolidada.
* Validação de consistência com planilhas manuais.
* Agendamento de execução (ex.: diário, semanal, mensal).

---

## 📌 Etapa 3 – Ambiente Gráfico (BI)

### 🎯 Objetivo

Oferecer ao usuário final um ambiente interativo para **exploração dos dados**, sem depender de planilhas fixas, permitindo criar relatórios personalizados.

### 📂 Escopo

* Desenvolvimento de um **painel gráfico (dashboard)** com base nos blocos de dados estruturados.
* Integração com ferramenta de **visualização (ex.: Power BI, Metabase ou solução web customizada)**.
* Implementação de filtros, comparativos e indicadores-chave (KPIs).

### ✅ Entregáveis

* Ambiente gráfico de fácil uso pelo setor de compras.
* Conjunto de dashboards padrão (estoque, fornecedores, metas, vendas).
* Documentação de uso e treinamento para equipe.

---

### 👉 Resumo

* Etapa 1: **blocos de dados estruturados**
* Etapa 2: **planilhas consolidadas automaticamente**
* Etapa 3: **ambiente BI interativo**

