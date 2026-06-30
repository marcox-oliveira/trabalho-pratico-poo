from models.base import EntidadeBase

class Album(EntidadeBase):
    def __init__(self, titulo: str, artista_id: int,
                 ano: int = None, id: int = None):
        self._id = id
        self._titulo = titulo
        self._artista_id = artista_id
        self._ano = ano

    @property
    def id(self):
        return self._id

    @property
    def titulo(self):
        return self._titulo

    @property
    def artista_id(self):
        return self._artista_id

    @property
    def ano(self):
        return self._ano

    def validar(self) -> None:
        if not self._titulo or not self._titulo.strip():
            raise ValueError("Título do álbum é obrigatório.")
        if not self._artista_id:
            raise ValueError("Artista é obrigatório para o álbum.")
        if self._ano and (self._ano < 1900 or self._ano > 2100):
            raise ValueError("Ano inválido.")

    def para_dict(self) -> dict:
        return {
            "id": self._id,
            "titulo": self._titulo,
            "artista_id": self._artista_id,
            "ano": self._ano,
        }

    def __str__(self) -> str:
        ano_str = f" ({self._ano})" if self._ano else ""
        return f"💿 {self._titulo}{ano_str} [artista_id={self._artista_id}]"
