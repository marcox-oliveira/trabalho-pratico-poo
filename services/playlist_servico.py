from models.playlist import Playlist
from repositories.playlist_repo import PlaylistRepositorio
from repositories.musica_repo import MusicaRepositorio

class PlaylistServico:
    def __init__(self):
        self._repo = PlaylistRepositorio()
        self._musica_repo = MusicaRepositorio()

    def criar(self, nome: str, usuario_id: int,
              descricao: str = None, publica: bool = False) -> Playlist:
        playlist = Playlist(nome=nome, usuario_id=usuario_id,
                            descricao=descricao, publica=publica)
        return self._repo.inserir(playlist)

    def listar_do_usuario(self, usuario_id: int) -> list:
        return self._repo.listar_por_usuario(usuario_id)

    def buscar_por_id(self, id_: int) -> Playlist:
        pl = self._repo.buscar_por_id(id_)
        if not pl:
            raise ValueError(f"Playlist id={id_} não encontrada.")
        return pl

    def adicionar_musica(self, playlist_id: int, musica_id: int,
                         usuario_id: int) -> None:
        pl = self.buscar_por_id(playlist_id)

        if pl.usuario_id != usuario_id:
            raise PermissionError("Somente o dono pode editar esta playlist.")

        if not self._musica_repo.buscar_por_id(musica_id):
            raise ValueError(f"Mídia id={musica_id} não encontrada.")

        ids_atuais = self._repo.listar_musicas_da_playlist(playlist_id)
        if musica_id in ids_atuais:
            raise ValueError("Esta mídia já está na playlist.")

        posicao = len(ids_atuais) + 1
        self._repo.adicionar_musica(playlist_id, musica_id, posicao)

    def remover_musica(self, playlist_id: int, musica_id: int,
                       usuario_id: int) -> None:
        pl = self.buscar_por_id(playlist_id)
        if pl.usuario_id != usuario_id:
            raise PermissionError("Somente o dono pode editar esta playlist.")
        self._repo.remover_musica(playlist_id, musica_id)

    def listar_midias(self, playlist_id: int) -> list:
        ids = self._repo.listar_musicas_da_playlist(playlist_id)
        midias = []
        for mid_id in ids:
            m = self._musica_repo.buscar_por_id(mid_id)
            if m:
                midias.append(m)
        return midias

    def atualizar(self, playlist_id: int, usuario_id: int,
                  nome: str = None, descricao: str = None,
                  publica: bool = None) -> None:
        pl = self.buscar_por_id(playlist_id)
        if pl.usuario_id != usuario_id:
            raise PermissionError("Somente o dono pode editar esta playlist.")
        if nome:
            pl._nome = nome
        if descricao is not None:
            pl._descricao = descricao
        if publica is not None:
            pl._publica = publica
        self._repo.atualizar(pl)

    def excluir(self, playlist_id: int, usuario_id: int) -> None:
        pl = self.buscar_por_id(playlist_id)
        if pl.usuario_id != usuario_id:
            raise PermissionError("Somente o dono pode excluir esta playlist.")
        self._repo.excluir(playlist_id)

    def registrar_reproducao(self, usuario_id: int, musica_id: int) -> None:
        self._repo.registrar_reproducao(usuario_id, musica_id)
