from database.conexao import obter_conexao, fechar_conexao
def criar_tabelas():
    conexao = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL,
                tipo VARCHAR(20) NOT NULL DEFAULT 'ouvinte',
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artistas (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                genero VARCHAR(80),
                pais VARCHAR(80),
                bio TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS albuns (
                id SERIAL PRIMARY KEY,
                titulo VARCHAR(200) NOT NULL,
                ano INTEGER,
                artista_id INTEGER NOT NULL REFERENCES artistas(id) ON DELETE CASCADE,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS musicas (
                id SERIAL PRIMARY KEY,
                titulo VARCHAR(200) NOT NULL,
                duracao_segundos INTEGER NOT NULL,
                genero VARCHAR(80),
                tipo VARCHAR(20) NOT NULL DEFAULT 'musica',
                album_id INTEGER REFERENCES albuns(id) ON DELETE SET NULL,
                artista_id INTEGER NOT NULL REFERENCES artistas(id) ON DELETE CASCADE,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(150) NOT NULL,
                descricao TEXT,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                publica BOOLEAN DEFAULT FALSE,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlist_musicas (
                playlist_id INTEGER NOT NULL REFERENCES playlists(id) ON DELETE CASCADE,
                musica_id INTEGER NOT NULL REFERENCES musicas(id) ON DELETE CASCADE,
                posicao INTEGER NOT NULL DEFAULT 1,
                PRIMARY KEY (playlist_id, musica_id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_reproducao (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                musica_id INTEGER NOT NULL REFERENCES musicas(id) ON DELETE CASCADE,
                reproduzido_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conexao.commit()
        print("✅ Tabelas criadas com sucesso!")

    except Exception as e:
        if conexao:
            conexao.rollback()
        raise RuntimeError(f"Erro ao criar tabelas: {e}")
    finally:
        fechar_conexao(conexao)
