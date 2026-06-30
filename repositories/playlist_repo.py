from database.conexao import obter_conexao, fechar_conexao
from models.playlist import Playlist

class PlaylistRepositorio:
    def _fabricar(self, row) -> Playlist:
        return Playlist(
            id=row[0], nome=row[1], usuario_id=row[2],
            descricao=row[3], publica=row[4]
        )

    def inserir(self, playlist: Playlist) -> Playlist:
        playlist.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO playlists (nome, descricao, usuario_id, publica)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (playlist.nome, playlist.descricao,
                 playlist.usuario_id, playlist.publica)
            )
            playlist._id = cursor.fetchone()[0]
            conexao.commit()
            return playlist
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao criar playlist: {e}")
        finally:
            fechar_conexao(conexao)

    def listar_por_usuario(self, usuario_id: int) -> list:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT id, nome, usuario_id, descricao, publica
                   FROM playlists WHERE usuario_id = %s ORDER BY nome""",
                (usuario_id,)
            )
            return [self._fabricar(row) for row in cursor.fetchall()]
        finally:
            fechar_conexao(conexao)

    def buscar_por_id(self, id_: int) -> Playlist | None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT id, nome, usuario_id, descricao, publica
                   FROM playlists WHERE id = %s""",
                (id_,)
            )
            row = cursor.fetchone()
            return self._fabricar(row) if row else None
        finally:
            fechar_conexao(conexao)

    def adicionar_musica(self, playlist_id: int, musica_id: int,
                         posicao: int = 1) -> None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO playlist_musicas (playlist_id, musica_id, posicao)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (playlist_id, musica_id) DO NOTHING""",
                (playlist_id, musica_id, posicao)
            )
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao adicionar música à playlist: {e}")
        finally:
            fechar_conexao(conexao)

    def remover_musica(self, playlist_id: int, musica_id: int) -> None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """DELETE FROM playlist_musicas
                   WHERE playlist_id=%s AND musica_id=%s""",
                (playlist_id, musica_id)
            )
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao remover música da playlist: {e}")
        finally:
            fechar_conexao(conexao)

    def listar_musicas_da_playlist(self, playlist_id: int) -> list:
        """Retorna IDs das músicas na playlist."""
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT musica_id FROM playlist_musicas
                   WHERE playlist_id = %s ORDER BY posicao""",
                (playlist_id,)
            )
            return [row[0] for row in cursor.fetchall()]
        finally:
            fechar_conexao(conexao)

    def atualizar(self, playlist: Playlist) -> None:
        playlist.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """UPDATE playlists SET nome=%s, descricao=%s, publica=%s
                   WHERE id=%s""",
                (playlist.nome, playlist.descricao,
                 playlist.publica, playlist.id)
            )
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao atualizar playlist: {e}")
        finally:
            fechar_conexao(conexao)

    def excluir(self, id_: int) -> None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM playlists WHERE id = %s", (id_,))
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao excluir playlist: {e}")
        finally:
            fechar_conexao(conexao)

    def registrar_reproducao(self, usuario_id: int, musica_id: int) -> None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO historico_reproducao (usuario_id, musica_id)
                   VALUES (%s, %s)""",
                (usuario_id, musica_id)
            )
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao registrar reprodução: {e}")
        finally:
            fechar_conexao(conexao)
