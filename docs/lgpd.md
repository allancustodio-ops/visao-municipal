# Nota LGPD – CSV com dados pessoais (CPF, nome, e-mail)

**Cenário:** o negócio envia um CSV de clientes com CPF, nome, e-mail e município, para
cruzar com o Panorama Municipal. Os princípios que guiam cada etapa são os do art. 6º da
LGPD, sobretudo **finalidade**, **necessidade** (usar só o mínimo) e **segurança**.
Em desenvolvimento e testes, uso apenas dados fictícios (Faker `pt_BR`), nunca reais.

**1. Antes da ingestão**
- Definir com o negócio e o encarregado (DPO) a finalidade (ex.: contar clientes por
  município) e a base legal (art. 7º). Sem finalidade definida, o dado não entra.
- Registrar a operação (art. 37) e classificar as colunas: CPF, nome e e-mail são dados
  pessoais; município é dado de apoio.

**2. Ingestão (Bronze restrita)**
- Lakehouse separado, só para dados pessoais, com acesso apenas da engenharia. O
  Panorama Municipal e o app não leem dessa área.
- Rótulo de confidencialidade no Purview ("Confidencial – dados pessoais").
- O CSV original fica com retenção curta: é apagado depois que a Silver é validada.
- Nunca no Git (`.gitignore`) e nunca em logs: o log registra contagens, não registros.

**3. Silver: pseudonimização e minimização**
- CPF normalizado e validado (dígitos verificadores) vira `id_cliente` =
  **HMAC-SHA256(CPF, chave secreta no Azure Key Vault)**. Um hash simples não basta: o
  CPF tem poucas combinações possíveis, e um atacante calcularia todas em minutos.
- Nome e e-mail são **removidos**. Se uma área precisar contatar o cliente, o contato
  fica numa tabela separada, com acesso restrito e finalidade própria.
- A ligação `id_cliente ↔ CPF` fica numa tabela restrita, usada só para atender os
  direitos do titular.
- Dado pseudonimizado **ainda é dado pessoal**, porque é reversível com a chave. Por
  isso, a Silver continua restrita.

**4. Gold e consumo**
- Só agregados por município (ex.: clientes por município, penetração sobre a
  população), sem nenhum identificador.
- **Supressão de grupos pequenos:** municípios com menos de 10 clientes aparecem
  agrupados, para evitar reidentificação. Com isso, a Gold se aproxima de dado
  anonimizado (art. 12).
- Modelo semântico com segurança por linha (RLS, ex.: gerente vê só a sua região) e por
  objeto (OLS) quando necessário. O app mantém o acesso restrito ao item (premissa 8).

**5. Direitos do titular, retenção e incidentes**
- Pedido de acesso ou eliminação (art. 18): a tabela restrita localiza o `id_cliente`. A
  exclusão no Delta exige `DELETE` **e** `VACUUM`, porque o histórico de versões (time
  travel) guarda os registros antigos.
- Política de retenção por camada, com expurgo automático.
- Segurança (art. 46): acesso mínimo, auditoria de acesso do Fabric e chave do HMAC com
  rotação. Em caso de incidente, plano de resposta e comunicação à ANPD e aos titulares
  (art. 48).

**Resumo do fluxo:** CSV → Bronze restrita (original, retenção curta) → Silver
(pseudonimizada, sem nome e e-mail) → Gold (agregada, sem identificadores) → modelo e app
(acesso restrito e RLS).
