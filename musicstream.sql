CREATE DATABASE musicstream
    WITH ENCODING 'UTF8'
    LC_COLLATE = 'pt_BR.UTF-8'
    LC_CTYPE = 'pt_BR.UTF-8'
    TEMPLATE template0;

\c musicstream

CREATE TABLE IF NOT EXISTS usuarios (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(100)  NOT NULL,
    email       VARCHAR(150)  NOT NULL UNIQUE,
    senha       VARCHAR(255)  NOT NULL,
    tipo        VARCHAR(20)   NOT NULL DEFAULT 'ouvinte',
    criado_em   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS artistas (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(150)  NOT NULL,
    genero      VARCHAR(80),
    pais        VARCHAR(80),
    bio         TEXT,
    criado_em   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS albuns (
    id          SERIAL PRIMARY KEY,
    titulo      VARCHAR(200)  NOT NULL,
    ano         INTEGER,
    artista_id  INTEGER       NOT NULL
                REFERENCES artistas(id) ON DELETE CASCADE,
    criado_em   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS musicas (
    id                  SERIAL PRIMARY KEY,
    titulo              VARCHAR(200)  NOT NULL,
    duracao_segundos    INTEGER       NOT NULL,
    genero              VARCHAR(80),
    tipo                VARCHAR(20)   NOT NULL DEFAULT 'musica',
    album_id            INTEGER       REFERENCES albuns(id) ON DELETE SET NULL,
    artista_id          INTEGER       NOT NULL
                        REFERENCES artistas(id) ON DELETE CASCADE,
    criado_em           TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS playlists (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(150)  NOT NULL,
    descricao   TEXT,
    usuario_id  INTEGER       NOT NULL
                REFERENCES usuarios(id) ON DELETE CASCADE,
    publica     BOOLEAN       DEFAULT FALSE,
    criado_em   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS playlist_musicas (
    playlist_id INTEGER  NOT NULL REFERENCES playlists(id)  ON DELETE CASCADE,
    musica_id   INTEGER  NOT NULL REFERENCES musicas(id)    ON DELETE CASCADE,
    posicao     INTEGER  NOT NULL DEFAULT 1,
    PRIMARY KEY (playlist_id, musica_id)
);

CREATE TABLE IF NOT EXISTS historico_reproducao (
    id              SERIAL PRIMARY KEY,
    usuario_id      INTEGER  NOT NULL REFERENCES usuarios(id)  ON DELETE CASCADE,
    musica_id       INTEGER  NOT NULL REFERENCES musicas(id)   ON DELETE CASCADE,
    reproduzido_em  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nome, email, senha, tipo) VALUES
    ('Admin',         'admin@musicstream.com', 'admin123', 'admin'),
    ('João Ouvinte',  'joao@email.com',        'joao123',  'ouvinte'),
    ('Maria Premium', 'maria@email.com',       'maria123', 'assinante');

INSERT INTO artistas (nome, genero, pais) VALUES
    ('The Beatles',   'Rock',     'Reino Unido'),
    ('Legião Urbana', 'Rock',     'Brasil'),
    ('Emicida',       'Hip-Hop',  'Brasil');

INSERT INTO albuns (titulo, artista_id, ano) VALUES
    ('Abbey Road',    1, 1969),
    ('Que País É Este', 2, 1987),
    ('AmarElo',       3, 2019);

INSERT INTO musicas (titulo, duracao_segundos, genero, tipo, album_id, artista_id) VALUES
    ('Come Together',       259, 'Rock',    'musica',  1, 1),
    ('Something',           182, 'Rock',    'musica',  1, 1),
    ('Que País É Este',     213, 'Rock',    'musica',  2, 2),
    ('Tempo Perdido',       316, 'Rock',    'musica',  2, 2),
    ('AmarElo',             207, 'Hip-Hop', 'musica',  3, 3),
    ('Podcast de Rock',    1800, 'Rock',    'podcast', NULL, 1);
