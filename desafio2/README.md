# Desafio 2 — Volumes e Persistência

## Descrição da Solução

Este desafio demonstra um dos conceitos mais importantes do Docker: **persistência de dados usando volumes**. A ideia é mostrar que, mesmo quando um container é removido, os dados armazenados em volumes Docker permanecem intactos e podem ser reutilizados por novos containers.

### Contexto

Por padrão, tudo dentro de um container é efêmero - quando você remove o container, tudo é perdido. Para aplicações que precisam manter dados (como bancos de dados), volumes são essenciais.

## Arquitetura e Decisões Técnicas

### Componente Principal: PostgreSQL

- **Banco de dados escolhido**: PostgreSQL 15
- **Volume nomeado**: `db_desafio2_data`
- **Ponto de montagem**: `/var/lib/postgresql/data` (diretório padrão de dados do Postgres)

### Por que PostgreSQL?

- É um banco relacional robusto e amplamente usado
- A imagem oficial do Docker Hub é bem mantida
- Perfeito para demonstrar persistência de dados estruturados

### Como funciona a persistência?

Quando criamos um volume Docker e o montamos em `/var/lib/postgresql/data`, todos os arquivos do banco (tabelas, índices, configurações) são armazenados **fora do container**, no sistema de arquivos do Docker host.

Isso significa:
- ✅ Remover o container NÃO apaga os dados
- ✅ Criar um novo container com o mesmo volume recupera todos os dados
- ✅ Os dados sobrevivem a reinicializações e atualizações de imagem

## Funcionamento Passo a Passo

### Ciclo de vida da demonstração:

1. **Criação do Volume**: Volume nomeado é criado pelo Docker
2. **Primeiro Container**: PostgreSQL inicia e cria estruturas no volume
3. **Inserção de Dados**: Criamos uma tabela e inserimos registros
4. **Remoção do Container**: Container é destruído (mas volume permanece!)
5. **Segundo Container**: Novo Postgres conecta ao mesmo volume
6. **Verificação**: Os dados inseridos anteriormente ainda estão lá!

```
Volume Docker (persiste)
         ↓
Container 1 → Cria tabela "pessoas" → Container removido
         ↓
Container 2 → SELECT * FROM pessoas → Dados ainda existem!
```

## Instruções de Execução

### Passo 1: Criar o volume

```bash
docker volume create db_desafio2_data
```

Você pode inspecionar o volume:

```bash
docker volume inspect db_desafio2_data
```

### Passo 2: Iniciar o primeiro container Postgres

```bash
docker run -d \
  --name desafio2-postgres \
  -e POSTGRES_USER=usuario_demo \
  -e POSTGRES_PASSWORD=senha_segura \
  -e POSTGRES_DB=banco_desafio2 \
  -v db_desafio2_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15
```

**Explicação dos parâmetros:**
- `-e POSTGRES_USER`: usuário do banco
- `-e POSTGRES_PASSWORD`: senha do usuário
- `-e POSTGRES_DB`: nome do banco a ser criado
- `-v db_desafio2_data:/var/lib/postgresql/data`: monta o volume no diretório de dados do Postgres
- `-p 5432:5432`: expõe a porta padrão do Postgres

### Passo 3: Criar uma tabela e inserir dados

Aguarde alguns segundos para o Postgres inicializar completamente, depois execute:

```bash
docker exec -it desafio2-postgres psql -U usuario_demo -d banco_desafio2 -c \
  "CREATE TABLE pessoas (id SERIAL PRIMARY KEY, nome TEXT, idade INT);"
```

Insira alguns registros:

```bash
docker exec -it desafio2-postgres psql -U usuario_demo -d banco_desafio2 -c \
  "INSERT INTO pessoas (nome, idade) VALUES ('Maria Silva', 28), ('João Santos', 35), ('Ana Costa', 22);"
```

Consulte os dados:

```bash
docker exec -it desafio2-postgres psql -U usuario_demo -d banco_desafio2 -c \
  "SELECT * FROM pessoas;"
```

Você verá algo como:

```
 id |     nome      | idade
----+---------------+-------
  1 | Maria Silva   |    28
  2 | João Santos   |    35
  3 | Ana Costa     |    22
```

### Passo 4: Remover o container (momento crítico!)

```bash
docker rm -f desafio2-postgres
```

O container foi destruído. Mas e os dados?

### Passo 5: Criar um novo container usando o mesmo volume

```bash
docker run -d \
  --name desafio2-postgres \
  -e POSTGRES_USER=usuario_demo \
  -e POSTGRES_PASSWORD=senha_segura \
  -e POSTGRES_DB=banco_desafio2 \
  -v db_desafio2_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15
```

Note que é exatamente o mesmo comando, conectando ao mesmo volume.

### Passo 6: Verificar que os dados persistiram

```bash
docker exec -it desafio2-postgres psql -U usuario_demo -d banco_desafio2 -c \
  "SELECT * FROM pessoas;"
```

**Resultado**: Os mesmos 3 registros estarão lá! 🎉

Isso prova que os dados sobreviveram à remoção do container.

## Limpeza Completa

Para remover tudo (incluindo o volume e seus dados):

```bash
docker rm -f desafio2-postgres
docker volume rm db_desafio2_data
```

⚠️ **Atenção**: Remover o volume apaga permanentemente todos os dados!

## Opcional: Container Adicional para Leitura

Você pode criar um segundo container simultaneamente para demonstrar que múltiplos containers podem acessar os mesmos dados (embora para Postgres isso não seja recomendado em produção):

```bash
docker run -it --rm \
  --network host \
  postgres:15 \
  psql -h localhost -U usuario_demo -d banco_desafio2 -c "SELECT * FROM pessoas;"
```

Este comando cria um container temporário apenas para executar uma query e depois se auto-remove.

## Estrutura de Arquivos

```
desafio2/
├── README.md
└── demo-persist.ps1  (script auxiliar para PowerShell)
```

## Conceitos Importantes

**Tipos de volumes no Docker:**

1. **Volumes nomeados** (usado neste desafio): Gerenciados pelo Docker, ideais para produção
2. **Bind mounts**: Montam um diretório específico do host
3. **Volumes anônimos**: Criados automaticamente, difíceis de gerenciar

**Por que usar volumes nomeados?**

- Docker gerencia a localização física
- Fácil backup e migração
- Melhor performance em alguns sistemas operacionais
- Isolamento entre diferentes projetos

Este desafio demonstra na prática por que volumes são fundamentais para aplicações stateful com Docker!
