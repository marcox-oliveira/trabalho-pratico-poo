# 🎶 MusicStream

Sistema de streaming de música desenvolvido em Python com PostgreSQL, utilizando Programação Orientada a Objetos.

---

## 👥 Integrantes do Grupo

> _Ebler_
> _Matheus Damasceno Glória_
> _Marcos de Oliveira da Silva_
> _Nádia Maria Leão Xavier_

---

## 📋 Descrição do Sistema

MusicStream é uma plataforma de streaming de música em linha de comando que permite:

- Cadastrar e gerenciar **usuários** (ouvintes gratuitos e assinantes premium)
- Cadastrar **artistas**, **álbuns**, **músicas** e **podcasts**
- Criar e gerenciar **playlists** pessoais
- Registrar histórico de reprodução

---

## 🏗️ Arquitetura e Conceitos de POO

### Classes de Domínio (`models/`)

| Classe        | Herda de        | Descrição                              |
|---------------|-----------------|----------------------------------------|
| `EntidadeBase`| `ABC`           | Classe abstrata base com `para_dict()` e `validar()` |
| `Usuario`     | `EntidadeBase`  | Usuário com encapsulamento (senha privada, properties) |
| `Ouvinte`     | `Usuario`       | Plano gratuito                         |
| `Assinante`   | `Usuario`       | Plano premium                          |
| `Midia`       | `EntidadeBase`  | Classe abstrata para mídias            |
| `Musica`      | `Midia`         | Faixa musical                          |
| `Podcast`     | `Midia`         | Episódio de podcast                    |
| `Artista`     | `EntidadeBase`  | Artista ou banda                       |
| `Album`       | `EntidadeBase`  | Álbum de um artista                    |
| `Playlist`    | `EntidadeBase`  | Playlist de um usuário                 |

### Pilares de POO Demonstrados

**Encapsulamento** — `Usuario` armazena a senha em atributo privado (`__senha`), exposto apenas pelos métodos `verificar_senha()` e `get_senha_hash()`.

**Herança** — duas hierarquias:
- `EntidadeBase → Usuario → Ouvinte / Assinante`
- `EntidadeBase → Midia → Musica / Podcast`

**Polimorfismo** — o método `reproduzir()` é chamado da mesma forma em `Musica` e `Podcast`, mas cada um retorna uma mensagem diferente. Idem para `descricao_plano()` em `Ouvinte` e `Assinante`.

**Classe Abstrata** — `EntidadeBase` (via `ABC`) define o contrato `para_dict()` e `validar()`. `Midia` acrescenta `reproduzir()` como método abstrato.

---

## 🗄️ Banco de Dados

### Tabelas

| Tabela                 | PK   | Relacionamentos                          |
|------------------------|------|------------------------------------------|
| `usuarios`             | `id` | —                                        |
| `artistas`             | `id` | —                                        |
| `albuns`               | `id` | FK → `artistas.id`                       |
| `musicas`              | `id` | FK → `artistas.id`, FK → `albuns.id`     |
| `playlists`            | `id` | FK → `usuarios.id`                       |
| `playlist_musicas`     | PK composta | FK → `playlists.id`, FK → `musicas.id` |
| `historico_reproducao` | `id` | FK → `usuarios.id`, FK → `musicas.id`   |

### Operações CRUD implementadas

Todas as entidades possuem: **INSERT**, **SELECT**, **UPDATE**, **DELETE**.

---

## 🚀 Instruções de Execução

### Pré-requisitos

- Python 3.10+
- PostgreSQL 13+
- Módulo `psycopg2`

```bash
pip install psycopg2-binary
```

### 1. Criar o banco de dados

**Opção A — via pgAdmin (recomendado no Windows):**
1. Crie um banco chamado `musicstream` (botão direito em *Databases* → *Create* → *Database*)
2. Selecione o banco criado e abra o *Query Tool*
3. Cole e execute o conteúdo de `musicstream.sql` (sem a linha `CREATE DATABASE` e sem `\c`, que são comandos exclusivos do terminal `psql`)

**Opção B — via terminal `psql`:**
```bash
psql -U postgres -f musicstream.sql
```

Ou deixar o próprio sistema criar as tabelas automaticamente na primeira execução (ver passo 3).

### 2. Configurar a conexão

Edite `database/conexao.py` com suas credenciais:

```python
conexao = psycopg2.connect(
    host="localhost",
    database="musicstream",
    user="postgres",
    password="SUA_SENHA",
    port=5432
)
```

### 3. Executar

```bash
cd musicstream
python main.py
```

As tabelas são criadas automaticamente na primeira execução. Se usar o script SQL, dados de exemplo já estão incluídos:

| E-mail                      | Senha      | Tipo       |
|-----------------------------|------------|------------|
| `admin@musicstream.com`     | `admin123` | admin      |
| `joao@email.com`            | `joao123`  | ouvinte    |
| `maria@email.com`           | `maria123` | assinante  |

---

## 📁 Estrutura do Projeto

```
musicstream/
│
├── main.py                  ← Ponto de entrada
├── musicstream.sql          ← Script SQL (criação + dados de exemplo)
├── README.md
│
├── database/
│   ├── conexao.py           ← Conexão com PostgreSQL
│   └── schema.py            ← Criação das tabelas
│
├── models/
│   ├── base.py              ← EntidadeBase (ABC)
│   ├── usuario.py           ← Usuario, Ouvinte, Assinante
│   ├── midia.py             ← Midia (ABC), Musica, Podcast
│   ├── artista.py           ← Artista
│   ├── album.py             ← Album
│   └── playlist.py          ← Playlist
│
├── repositories/
│   ├── usuario_repo.py      ← CRUD de usuários
│   ├── artista_repo.py      ← CRUD de artistas
│   ├── album_repo.py        ← CRUD de álbuns
│   ├── musica_repo.py       ← CRUD de mídias
│   └── playlist_repo.py     ← CRUD de playlists
│
├── services/
│   ├── usuario_servico.py   ← Regras de negócio (e-mail único, autenticação)
│   ├── musica_servico.py    ← Regras de negócio (polimorfismo reproduzir)
│   └── playlist_servico.py  ← Regras de negócio (dono, sem duplicatas)
│
└── ui/
    ├── helpers.py           ← Funções auxiliares de terminal
    ├── menu_usuarios.py
    ├── menu_musicas.py
    ├── menu_artistas.py
    └── menu_playlists.py
```

---

## ✅ Regras de Negócio Implementadas

- Não permitir cadastro com e-mail já existente
- Autenticação por e-mail e senha (senha encapsulada)
- Somente o dono da playlist pode editar ou excluir
- Não permitir a mesma música duas vezes na mesma playlist
- Promoção de ouvinte para assinante premium
