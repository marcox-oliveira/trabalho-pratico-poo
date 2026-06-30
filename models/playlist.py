from models.base import EntidadeBase

class Playlist(EntidadeBase):
    def __init__(self, nome: str, usuario_id: int,
                 descricao: str = None, publica: bool = False,
                 id: int = None):
        self._id = id
        self._nome = nome
        self._usuario_id = usuario_id
        self._descricao = descricao
        self._publica = publica
        self._musicas: list = []

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def usuario_id(self):
        return self._usuario_id

    @property
    def descricao(self):
        return self._descricao

    @property
    def publica(self):
        return self._publica

    @property
    def musicas(self):
        return list(self._musicas)

    def adicionar_midia(self, midia) -> None:
        self._musicas.append(midia)

    def total_duracao(self) -> int:
        return sum(m.duracao_segundos for m in self._musicas)

    def duracao_formatada(self) -> str:
        total = self.total_duracao()
        horas = total // 3600
        minutos = (total % 3600) // 60
        segundos = total % 60
        if horas:
            return f"{horas}h {minutos:02d}min {segundos:02d}s"
        return f"{minutos:02d}min {segundos:02d}s"

    def validar(self) -> None:
        if not self._nome or not self._nome.strip():
            raise ValueError("Nome da playlist é obrigatório.")
        if not self._usuario_id:
            raise ValueError("Usuário é obrigatório para a playlist.")

    def para_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "usuario_id": self._usuario_id,
            "descricao": self._descricao,
            "publica": self._publica,
        }

    def __str__(self) -> str:
        vis = "🌐 Pública" if self._publica else "🔒 Privada"
        return f"📋 {self._nome} [{vis}] — {len(self._musicas)} faixa(s)"
