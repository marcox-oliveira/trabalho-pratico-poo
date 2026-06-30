from models.base import EntidadeBase

class Artista(EntidadeBase):
    def __init__(self, nome: str, genero: str = None,
                 pais: str = None, bio: str = None, id: int = None):
        self._id = id
        self._nome = nome
        self._genero = genero
        self._pais = pais
        self._bio = bio

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome do artista não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def genero(self):
        return self._genero

    @property
    def pais(self):
        return self._pais

    @property
    def bio(self):
        return self._bio

    def validar(self) -> None:
        if not self._nome or not self._nome.strip():
            raise ValueError("Nome do artista é obrigatório.")

    def para_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "genero": self._genero,
            "pais": self._pais,
            "bio": self._bio,
        }

    def __str__(self) -> str:
        partes = [f"🎤 {self._nome}"]
        if self._genero:
            partes.append(f"Gênero: {self._genero}")
        if self._pais:
            partes.append(f"País: {self._pais}")
        return " | ".join(partes)
