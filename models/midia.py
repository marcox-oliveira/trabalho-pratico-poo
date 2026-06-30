from abc import abstractmethod
from models.base import EntidadeBase

class Midia(EntidadeBase):
    def __init__(self, titulo: str, duracao_segundos: int,
                 genero: str = None, artista_id: int = None,
                 album_id: int = None, id: int = None, tipo: str = "midia"):
        self._id = id
        self._titulo = titulo
        self._duracao_segundos = duracao_segundos
        self._genero = genero
        self._artista_id = artista_id
        self._album_id = album_id
        self._tipo = tipo

    @property
    def id(self):
        return self._id

    @property
    def titulo(self):
        return self._titulo

    @property
    def duracao_segundos(self):
        return self._duracao_segundos

    @property
    def genero(self):
        return self._genero

    @property
    def artista_id(self):
        return self._artista_id

    @property
    def album_id(self):
        return self._album_id

    @property
    def tipo(self):
        return self._tipo

    def duracao_formatada(self) -> str:
        minutos = self._duracao_segundos // 60
        segundos = self._duracao_segundos % 60
        return f"{minutos:02d}:{segundos:02d}"

    @abstractmethod
    def reproduzir(self) -> str:
        pass

    def validar(self) -> None:
        if not self._titulo or not self._titulo.strip():
            raise ValueError("Título é obrigatório.")
        if self._duracao_segundos <= 0:
            raise ValueError("Duração deve ser maior que zero.")
        if not self._artista_id:
            raise ValueError("Artista é obrigatório.")

    def para_dict(self) -> dict:
        return {
            "id": self._id,
            "titulo": self._titulo,
            "duracao_segundos": self._duracao_segundos,
            "duracao_formatada": self.duracao_formatada(),
            "genero": self._genero,
            "artista_id": self._artista_id,
            "album_id": self._album_id,
            "tipo": self._tipo,
        }

    def __str__(self) -> str:
        return f"{self._titulo} [{self.duracao_formatada()}]"


class Musica(Midia):
    def __init__(self, titulo: str, duracao_segundos: int,
                 genero: str = None, artista_id: int = None,
                 album_id: int = None, id: int = None):
        super().__init__(titulo, duracao_segundos, genero,
                         artista_id, album_id, id, tipo="musica")

    def reproduzir(self) -> str:
        return f"🎵 Reproduzindo música: {self._titulo} ({self.duracao_formatada()})"

    def __str__(self) -> str:
        return f"🎵 {self._titulo} [{self.duracao_formatada()}] — tipo: música"


class Podcast(Midia):
    def __init__(self, titulo: str, duracao_segundos: int,
                 genero: str = None, artista_id: int = None,
                 album_id: int = None, id: int = None):
        super().__init__(titulo, duracao_segundos, genero,
                         artista_id, album_id, id, tipo="podcast")

    def reproduzir(self) -> str:
        return f"🎙️ Reproduzindo podcast: {self._titulo} ({self.duracao_formatada()})"

    def __str__(self) -> str:
        return f"🎙️ {self._titulo} [{self.duracao_formatada()}] — tipo: podcast"
