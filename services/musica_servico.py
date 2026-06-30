from models.midia import Musica, Podcast, Midia
from models.artista import Artista
from models.album import Album
from repositories.musica_repo import MusicaRepositorio
from repositories.artista_repo import ArtistaRepositorio
from repositories.album_repo import AlbumRepositorio

class MusicaServico:
    def __init__(self):
        self._repo = MusicaRepositorio()
        self._artista_repo = ArtistaRepositorio()
        self._album_repo = AlbumRepositorio()

    def cadastrar_artista(self, nome: str, genero: str = None,
                          pais: str = None, bio: str = None) -> Artista:
        artista = Artista(nome=nome, genero=genero, pais=pais, bio=bio)
        return self._artista_repo.inserir(artista)

    def listar_artistas(self) -> list:
        return self._artista_repo.listar()

    def buscar_artistas(self, nome: str) -> list:
        return self._artista_repo.buscar_por_nome(nome)

    def atualizar_artista(self, id_: int, nome: str = None,
                          genero: str = None, pais: str = None,
                          bio: str = None) -> None:
        artista = self._artista_repo.buscar_por_id(id_)
        if not artista:
            raise ValueError(f"Artista id={id_} não encontrado.")
        artista._nome = nome or artista.nome
        artista._genero = genero if genero is not None else artista.genero
        artista._pais = pais if pais is not None else artista.pais
        artista._bio = bio if bio is not None else artista.bio
        self._artista_repo.atualizar(artista)

    def excluir_artista(self, id_: int) -> None:
        if not self._artista_repo.buscar_por_id(id_):
            raise ValueError(f"Artista id={id_} não encontrado.")
        self._artista_repo.excluir(id_)

    def cadastrar_album(self, titulo: str, artista_id: int,
                        ano: int = None) -> Album:
        if not self._artista_repo.buscar_por_id(artista_id):
            raise ValueError("Artista não encontrado.")
        album = Album(titulo=titulo, artista_id=artista_id, ano=ano)
        return self._album_repo.inserir(album)

    def listar_albuns(self) -> list:
        return self._album_repo.listar()

    def albuns_do_artista(self, artista_id: int) -> list:
        return self._album_repo.buscar_por_artista(artista_id)

    def excluir_album(self, id_: int) -> None:
        if not self._album_repo.buscar_por_id(id_):
            raise ValueError(f"Álbum id={id_} não encontrado.")
        self._album_repo.excluir(id_)

    def cadastrar_musica(self, titulo: str, duracao: int, artista_id: int,
                         genero: str = None, album_id: int = None) -> Musica:
        self._validar_artista(artista_id)
        midia = Musica(titulo=titulo, duracao_segundos=duracao,
                       genero=genero, artista_id=artista_id,
                       album_id=album_id)
        return self._repo.inserir(midia)

    def cadastrar_podcast(self, titulo: str, duracao: int, artista_id: int,
                          genero: str = None, album_id: int = None) -> Podcast:
        self._validar_artista(artista_id)
        midia = Podcast(titulo=titulo, duracao_segundos=duracao,
                        genero=genero, artista_id=artista_id,
                        album_id=album_id)
        return self._repo.inserir(midia)

    def listar_midias(self) -> list:
        return self._repo.listar()

    def buscar_por_titulo(self, titulo: str) -> list:
        return self._repo.buscar_por_titulo(titulo)

    def buscar_por_id(self, id_: int) -> Midia:
        m = self._repo.buscar_por_id(id_)
        if not m:
            raise ValueError(f"Mídia id={id_} não encontrada.")
        return m

    def atualizar_midia(self, id_: int, titulo: str = None,
                        duracao: int = None, genero: str = None) -> None:
        midia = self.buscar_por_id(id_)
        if titulo:
            midia._titulo = titulo
        if duracao:
            midia._duracao_segundos = duracao
        if genero is not None:
            midia._genero = genero
        self._repo.atualizar(midia)

    def excluir_midia(self, id_: int) -> None:
        self.buscar_por_id(id_)
        self._repo.excluir(id_)

    def reproduzir(self, midia: Midia) -> str:
        return midia.reproduzir()

    def _validar_artista(self, artista_id: int) -> None:
        if not self._artista_repo.buscar_por_id(artista_id):
            raise ValueError(f"Artista id={artista_id} não encontrado.")
