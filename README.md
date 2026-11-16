# Panorama Municipal

Produto de dados (Bronze → Silver → Gold → modelo semântico) com dados públicos do IBGE/SIDRA
e um Fabric App analítico que consome o modelo. Desafio técnico – Analista de Dados Sênior.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `pipeline/` | Scripts das camadas (01_bronze, 02_silver, 03_qualidade, 04_gold) |
| `sql/` | Consultas analíticas com CTE e window functions |
| `semantic-model/` | Definição do modelo semântico e medidas DAX |
| `app/` | Fabric App `visao-municipal` (template dataapp do Rayfin) |
| `docs/` | Premissas, relatório de qualidade, modelo, LGPD e diário |
| `data/` | Dados gerados localmente (fora do Git) |

## Pré-requisitos

> No Windows, mantenha o projeto fora do OneDrive (ex.: `C:\dev`). Se o PowerShell bloquear o npm, rode
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` ou use o Prompt de Comando.


- Python 3.11+
- Node.js LTS (para o Fabric App)
- Acesso a um workspace do Fabric com capacidade e Fabric Apps habilitado

## Como rodar (local)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python pipeline/01_bronze_ingestao.py                # todas as fontes e anos
python pipeline/01_bronze_ingestao.py --anos 2021    # teste rápido com um ano
```

Saída: `data/bronze/raw/<fonte>/<ano>.json` (resposta original da API),
`data/bronze/<fonte>/<fonte>.parquet` e um log em `logs/`.

## Fabric App (visao-municipal)

- Workspace: **A minha área de trabalho** (My workspace). Ver premissa 5 em `docs/PREMISSAS.md`.
- Item: **visao-municipal** (tipo "Aplicação" na interface em português)
- ID do item: `cfdd4909-9f3a-4638-b033-d5b549dc6ab4`
- Acesso: só quem tem permissão no item (login pelo portal)
- Código: pasta `app/visao-municipal/`

### Como abrir

Abra pelo portal: **Áreas de trabalho → A minha área de trabalho → visao-municipal**.
A URL direta (`https://fit-flame-ef120c4f60-southcentralus.webapp.fabricapps.net`) não funciona
numa aba avulsa, porque o login é feito pelo portal do Fabric.

### Como rodar localmente e publicar

```bash
# criação (uma vez), a partir da pasta app/
npm create @microsoft/rayfin@latest -- "visao-municipal" --template dataapp --workspace "My workspace"

cd app/visao-municipal
npm install
npx rayfin up      # na primeira vez, ANTES do dev: gera as variáveis de ambiente do backend
npm run dev        # testa localmente em http://localhost:5173
npx rayfin up      # publica as alterações
```

## Estado da entrega e próximos passos

| Componente | Estado | Onde |
|---|---|---|
| Bronze, Silver, Qualidade e Gold | Concluído e validado no Fabric | `pipeline/fabric/01` a `04`, Lakehouse `lake_visao` |
| Relatório de qualidade | 24 PASS · 7 WARN · 0 FAIL | `docs/relatorio_qualidade.md` |
| Consultas SQL (CTE + window functions) | Concluído, executadas no ponto de extremidade SQL | `sql/` |
| Modelo semântico e medidas DAX | Concluído e validado (PIB per capita 2021 = R$ 42.247,52) | `semantic-model/` |
| Visões da diretoria | Relatório do Power BI Desktop com 2 páginas: visão executiva (indicadores, drill-down, mapa e tabela) e Insight (respostas calculadas pelo próprio modelo) | `semantic-model/sm_visao_municipal.pbix` (dados em `semantic-model/dados/`) |
| Fabric App `visao-municipal` | Criado, executado localmente e publicado; **falta ligar ao modelo** | `app/visao-municipal/` |

### Por que o app não está ligado ao modelo

1. O tenant não permite modelo Direct Lake em "A minha área de trabalho" nem a criação de
   workspaces; o modelo foi feito em modo Import no Power BI Desktop (premissa 16).
2. Na reta final, a conta corporativa passou a exigir MFA (Microsoft Authenticator) sem
   acesso ao aplicativo. Sem login, não foi possível publicar o modelo nem rodar o CLI do
   Rayfin. O modelo passou a ler cópias em Excel das tabelas Gold, com a mesma validação
   DAX (premissa 17).

### O que o relatório responde

As consultas SQL descobriram o insight; o relatório passou a calculá-lo sozinho, com
medidas DAX que respeitam os filtros de ano, região e UF (`semantic-model/medidas.dax`):

| Pergunta de negócio | Medidas | Validação (2021, Brasil) |
|---|---|---|
| Onde está concentrado o mercado? | Municípios para 50% do PIB · % dos municípios no núcleo · % da população no núcleo | 87 · 1,56% · 36,66%, iguais à consulta `sql/04_concentracao_pib.sql` |
| Para onde expandir? | Posição per capita na UF (até 3) · Atende porte mínimo (parâmetro ajustável na segmentação) | Mesmos municípios da consulta `sql/01_ranking_pib_per_capita_uf.sql` |

O mapa usa latitude e longitude de `semantic-model/dados/municipios_coordenadas.xlsx`
(premissa 18), unidas à dimensão de município no Power Query.

### Como abrir o relatório do Power BI

Abra `semantic-model/sm_visao_municipal.pbix`. Os dados vêm dos arquivos Excel em
`semantic-model/dados/` (cópias das tabelas Gold). O Power BI guarda o caminho completo
dos arquivos: se o repositório estiver em outra pasta que não `C:\dev\visao-municipal`,
use **Transformar dados → Definições da origem de dados → Alterar origem** e aponte para
os arquivos de `semantic-model/dados/`.

### Como completar o app quando o acesso voltar

1. **Voltar o modelo para o Lakehouse:** no Power BI Desktop, em Transformar dados →
   Definições da origem de dados, trocar os arquivos Excel pelo ponto de extremidade SQL
   do `lake_visao`. Rodar a consulta DAX de validação (`semantic-model/medidas.dax`):
   2021 deve dar 42.247,52.
2. **Publicar** o `sm_visao_municipal` em "A minha área de trabalho".
3. **Ligar o app ao modelo** (a partir de `app/visao-municipal`):
   ```bash
   # ID do workspace: está em rayfin/.env (gerado pelo npx rayfin up)
   npx rayfin connector search --workspace-id <ID_WORKSPACE> --type fabric-semanticmodel --json
   npx rayfin connector add --type fabric-semanticmodel --workspace-id <ID_WORKSPACE> \
       --item-id <ID_DO_MODELO> --name panoramaModel --operations executeQuery
   ```
4. **Montar as telas** reaproveitando as consultas DAX já validadas:
   - KPIs: `[PIB (R$)]`, `[População]`, `[PIB per capita (R$)]`, `[Variação PIB YoY %]`,
     `[Municípios]`, filtrados por ano e UF;
   - gráfico com drill-down pela hierarquia Geografia (região → UF → município);
   - tabela detalhada por município;
   - card com o insight da consulta `sql/04_concentracao_pib.sql`.
5. Testar com `npm run dev` e publicar com `npx rayfin up`. Abrir sempre pelo item
   `visao-municipal` no workspace (a URL direta não autentica).

Estimativa: menos de 1 hora para os passos 1 a 3; as telas reaproveitam o layout do
relatório do Power BI.

## Local × Fabric

| Aspecto | Local | Fabric |
|---|---|---|
| Armazenamento | Parquet em `data/` | Tabelas Delta no Lakehouse (OneLake) |
| Processamento | pandas / DuckDB | Notebook PySpark |
| Orquestração | execução manual | Data Pipeline agendado |
| Consumo | DuckDB | SQL endpoint + modelo semântico Direct Lake |
| Governança | – | Permissões de workspace, sensitivity labels, Purview |
