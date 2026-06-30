from database.conexao import obter_conexao, fechar_conexao
from models.midia import Musica, Podcast, Midia

class MusicaRepositorio:
    def _fabricar(self, row) -> Midia:
        id_, titulo, duracao, genero, tipo, album_id, artista_id = (
            row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        )
        if tipo == "podcast":
            return Podcast(titulo=titulo, duracao_segundos=duracao,
                           genero=genero, artista_id=artista_id,
                           album_id=album_id, id=id_)
        return Musica(titulo=titulo, duracao_segundos=duracao,
                      genero=genero, artista_id=artista_id,
                      album_id=album_id, id=id_)

    def inserir(self, midia: Midia) -> Midia:
        midia.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO musicas (titulo, duracao_segundos, genero, tipo,
                                       album_id, artista_id)
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
                (midia.titulo, midia.duracao_segundos, midia.genero,
                 midia.tipo, midia.album_id, midia.artista_id)
            )
            midia._id = cursor.fetchone()[0]
            conexao.commit()
            return midia
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao inserir mídia: {e}")
        finally:
            fechar_conexao(conexao)

    def listar(self) -> list:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT m.id, m.titulo, m.duracao_segundos, m.genero,
                          m.tipo, m.album_id, m.artista_id
                   FROM musicas m
                   ORDER BY m.titulo"""
            )
            return [self._fabricar(row) for row in cursor.fetchall()]
        finally:
            fechar_conexao(conexao)

    def buscar_por_titulo(self, titulo: str) -> list:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT id, titulo, duracao_segundos, genero, tipo,
                          album_id, artista_id
                   FROM musicas WHERE titulo ILIKE %s ORDER BY titulo""",
                (f"%{titulo}%",)
            )
            return [self._fabricar(row) for row in cursor.fetchall()]
        finally:
            fechar_conexao(conexao)

    def buscar_por_artista(self, artista_id: int) -> list:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT id, titulo, duracao_segundos, genero, tipo,
                          album_id, artista_id
                   FROM musicas WHERE artista_id = %s ORDER BY titulo""",
                (artista_id,)
            )
            return [self._fabricar(row) for row in cursor.fetchall()]
        finally:
            fechar_conexao(conexao)

    def buscar_por_id(self, id_: int) -> Midia | None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT id, titulo, duracao_segundos, genero, tipo,
                          album_id, artista_id
                   FROM musicas WHERE id = %s""",
                (id_,)
            )
            row = cursor.fetchone()
            return self._fabricar(row) if row else None
        finally:
            fechar_conexao(conexao)

    def atualizar(self, midia: Midia) -> None:
        midia.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """UPDATE musicas SET titulo=%s, duracao_segundos=%s,
                   genero=%s, tipo=%s, album_id=%s, artista_id=%s WHERE id=%s""",
                (midia.titulo, midia.duracao_segundos, midia.genero,
                 midia.tipo, midia.album_id, midia.artista_id, midia.id)
            )
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao atualizar mídia: {e}")
        finally:
            fechar_conexao(conexao)

    def excluir(self, id_: int) -> None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM musicas WHERE id = %s", (id_,))
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao excluir mídia: {e}")
        finally:
            fechar_conexao(conexao)
