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

## Local × Fabric

| Aspecto | Local | Fabric |
|---|---|---|
| Armazenamento | Parquet em `data/` | Tabelas Delta no Lakehouse (OneLake) |
| Processamento | pandas / DuckDB | Notebook PySpark |
| Orquestração | execução manual | Data Pipeline agendado |
| Consumo | DuckDB | SQL endpoint + modelo semântico Direct Lake |
| Governança | – | Permissões de workspace, sensitivity labels, Purview |
