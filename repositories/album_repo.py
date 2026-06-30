from database.conexao import obter_conexao, fechar_conexao
from models.album import Album

class AlbumRepositorio:
    def _fabricar(self, row) -> Album:
        return Album(id=row[0], titulo=row[1], artista_id=row[2], ano=row[3])

    def inserir(self, album: Album) -> Album:
        album.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO albuns (titulo, artista_id, ano)
                   VALUES (%s, %s, %s) RETURNING id""",
                (album.titulo, album.artista_id, album.ano)
            )
            album._id = cursor.fetchone()[0]
            conexao.commit()
            return album
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao inserir álbum: {e}")
        finally:
            fechar_conexao(conexao)

    def listar(self) -> list:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT a.id, a.titulo, a.artista_id, a.ano
                   FROM albuns a ORDER BY a.titulo"""
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
                """SELECT id, titulo, artista_id, ano FROM albuns
                   WHERE artista_id = %s ORDER BY ano""",
                (artista_id,)
            )
            return [self._fabricar(row) for row in cursor.fetchall()]
        finally:
            fechar_conexao(conexao)

    def buscar_por_id(self, id_: int) -> Album | None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, titulo, artista_id, ano FROM albuns WHERE id = %s",
                (id_,)
            )
            row = cursor.fetchone()
            return self._fabricar(row) if row else None
        finally:
            fechar_conexao(conexao)

    def atualizar(self, album: Album) -> None:
        album.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE albuns SET titulo=%s, artista_id=%s, ano=%s WHERE id=%s",
                (album.titulo, album.artista_id, album.ano, album.id)
            )
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao atualizar álbum: {e}")
        finally:
            fechar_conexao(conexao)

    def excluir(self, id_: int) -> None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM albuns WHERE id = %s", (id_,))
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao excluir álbum: {e}")
        finally:
            fechar_conexao(conexao)
