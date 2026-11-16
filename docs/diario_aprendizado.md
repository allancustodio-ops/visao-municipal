# Diário de aprendizado – Fabric App e Panorama Municipal

Versão resumida (entregável). O registro completo, com cada tentativa e erro, está em
`docs/DIARIO.md`.

## 1. Como aprendi o Fabric App

**Ordem das fontes**
1. PDF do desafio, para separar o que era obrigatório do que era opcional.
2. Documentação oficial em learn.microsoft.com/fabric/apps: visão geral, quickstart
   (`create-app`) e o template de app ligado a modelo semântico (`data-apps-template`).
3. Os passos que o próprio portal mostra ao criar o item, comparados com a documentação.
4. Artigos da comunidade sobre Rayfin, só para contexto, depois da documentação oficial.

**Tempo aproximado**

| Bloco | Tempo |
|---|---|
| Leitura do desafio e plano | 0,5 h |
| Fabric App: achar o recurso, criar, rodar e publicar | 2,5 h |
| Bronze, Silver, qualidade e Gold no Fabric | 3,5 h |
| SQL, modelo semântico e medidas DAX | 2 h |
| Contornar bloqueios de ambiente e montar o relatório | 2 h |

**O que tentei e descartei**
- Template `blankapp`, sugerido pelo portal: troquei pelo `dataapp`, feito para consumir
  modelo semântico.
- Um plano B com app local consultando o modelo pela API do Power BI: descartei quando
  descobri que o recurso estava disponível (ver obstáculo 1).
- Criar os itens no workspace VPN-DEV: sem permissão de criação.
- Modelo Direct Lake: bloqueado no meu ambiente (obstáculo 7).

## 2. Principais obstáculos

| # | Obstáculo | Como resolvi |
|---|---|---|
| 1 | O item "App" não aparecia | A interface em português o chama de **"Aplicação"**; confirmei pela descrição do card |
| 2 | VPN-DEV sem permissão | Projeto inteiro em "A minha área de trabalho", documentado como premissa |
| 3 | PowerShell bloqueando o npm; projeto no OneDrive | Política de execução por usuário; projeto movido para `C:\dev` |
| 4 | `npm run dev` abria página em branco | Console do navegador: faltavam variáveis de ambiente. O `npx rayfin up` precisa rodar antes do primeiro `dev` |
| 5 | URL do app não abria | O app autentica pelo portal; só abre pelo item no workspace |
| 6 | Rayfin criou um repositório Git dentro do app | Removi e mantive um único repositório na raiz |
| 7 | API de metadados do IBGE sem resposta a partir do Fabric | Passei a obter a lista de anos pela própria API SIDRA |
| 8 | PIB negativo bloqueou o portão de qualidade | Conferi o valor original: é dado oficial (Guamaré-RN, 2012). A regra virou alerta documentado |
| 9 | Modelo Direct Lake sem workspace de destino e criação de workspace bloqueada | Modelo em modo Import no Power BI Desktop |
| 10 | Autenticação multifator (MFA) sem acesso ao aplicativo | Tabelas Gold exportadas para Excel e relatório montado no Power BI |

**Não resolvido:** ligar o Fabric App ao modelo semântico. O app foi criado, rodou
localmente e foi publicado, mas o conector depende de publicar o modelo, o que o MFA
impediu. O passo que falta (`npx rayfin connector add`) está descrito no README.

**O que eu repensei:** no fim, percebi que o painel só mostrava números e quem
respondia as perguntas eram as consultas SQL. Levei essa lógica para medidas DAX, que
recalculam o núcleo de municípios e os candidatos à expansão conforme os filtros. Com
2021 e sem filtros, as medidas deram 87, 1,56% e 36,66%, iguais à consulta SQL.

## 3. Como usei IA generativa e como validei

Usei um assistente de IA como par de trabalho: plano de execução, primeira versão dos
notebooks, consultas SQL e medidas DAX, e diagnóstico de erros a partir de prints.

**Como validei**
- **Reconciliação entre camadas:** contagens da Bronze = Silver + cabeçalhos; totais da
  Gold iguais aos da Silver.
- **Portão de qualidade:** 31 regras (24 PASS, 7 WARN, 0 FAIL na execução final).
- **Mesma resposta por caminhos diferentes:** PIB per capita de 2021 igual no notebook da
  Gold e na medida DAX (R$ 42.247,52).
- **Fonte original:** sempre que algo parecia estranho, consultei o valor bruto do IBGE.

**Onde a IA errou e eu corrigi**
- Diagnosticou o item ausente como problema de região. Era só o nome traduzido.
- Indicou um caminho de menu do notebook que não existe mais na interface atual.
- Supôs a posição das colunas do SIDRA (`D3N` como variável); o cabeçalho mostrou outra
  ordem.
- Supôs que PIB nunca é negativo; o dado oficial mostrou o contrário.

**Quando recusei sugestões:** a IA propôs deixar o notebook tolerante a um erro meu de
parâmetro e mudar a lógica de novas tentativas. Recusei: o erro era meu, e preferi um
código simples que eu consigo explicar.

## 4. O que faria diferente e o que ainda não entendo bem

**Com mais tempo**
- Confirmar no primeiro dia: MFA disponível, permissões no workspace e se posso criar
  workspaces.
- Modelo Direct Lake num workspace compartilhado, salvo em formato PBIP (texto,
  versionável).
- Ligar o app ao modelo e montar as telas nele.
- Completar a série com a população dos Censos 2010 e 2022, tratando a quebra de
  metodologia.
- Agendar o pipeline e incluir indicadores de renda, já que PIB mede produção.

**O que ainda não entendo bem**
- Como o Rayfin gera e usa as variáveis de ambiente, e por que o `dev` depende do `up`.
- Limites de desempenho do conector de modelo semântico (`executeQuery`).
- Por que "A minha área de trabalho" não aceita modelo Direct Lake.
- Os detalhes da metodologia do PIB municipal que levam a valores negativos.
