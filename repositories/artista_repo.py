from database.conexao import obter_conexao, fechar_conexao
from models.artista import Artista

class ArtistaRepositorio:
    def _fabricar(self, row) -> Artista:
        return Artista(id=row[0], nome=row[1], genero=row[2],
                       pais=row[3], bio=row[4])

    def inserir(self, artista: Artista) -> Artista:
        artista.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO artistas (nome, genero, pais, bio)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (artista.nome, artista.genero, artista.pais, artista.bio)
            )
            artista._id = cursor.fetchone()[0]
            conexao.commit()
            return artista
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao inserir artista: {e}")
        finally:
            fechar_conexao(conexao)

    def listar(self) -> list:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, genero, pais, bio FROM artistas ORDER BY nome"
            )
            return [self._fabricar(row) for row in cursor.fetchall()]
        finally:
            fechar_conexao(conexao)

    def buscar_por_id(self, id_: int) -> Artista | None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, genero, pais, bio FROM artistas WHERE id = %s",
                (id_,)
            )
            row = cursor.fetchone()
            return self._fabricar(row) if row else None
        finally:
            fechar_conexao(conexao)

    def buscar_por_nome(self, nome: str) -> list:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT id, nome, genero, pais, bio FROM artistas
                   WHERE nome ILIKE %s ORDER BY nome""",
                (f"%{nome}%",)
            )
            return [self._fabricar(row) for row in cursor.fetchall()]
        finally:
            fechar_conexao(conexao)

    def atualizar(self, artista: Artista) -> None:
        artista.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """UPDATE artistas SET nome=%s, genero=%s, pais=%s, bio=%s
                   WHERE id=%s""",
                (artista.nome, artista.genero, artista.pais,
                 artista.bio, artista.id)
            )
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao atualizar artista: {e}")
        finally:
            fechar_conexao(conexao)

    def excluir(self, id_: int) -> None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM artistas WHERE id = %s", (id_,))
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao excluir artista: {e}")
        finally:
            fechar_conexao(conexao)
