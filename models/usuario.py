from models.base import EntidadeBase

class Usuario(EntidadeBase):
    TIPOS_VALIDOS = ("ouvinte", "assinante", "admin")

    def __init__(self, nome: str, email: str, senha: str,
                 tipo: str = "ouvinte", id: int = None):
        self._id = id
        self._nome = nome
        self._email = email
        self.__senha = senha
        self._tipo = tipo

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValueError("E-mail inválido.")
        self._email = valor.strip().lower()

    @property
    def tipo(self):
        return self._tipo

    def verificar_senha(self, senha: str) -> bool:
        return self.__senha == senha

    def alterar_senha(self, senha_atual: str, nova_senha: str) -> None:
        if not self.verificar_senha(senha_atual):
            raise ValueError("Senha atual incorreta.")
        if len(nova_senha) < 6:
            raise ValueError("Nova senha deve ter ao menos 6 caracteres.")
        self.__senha = nova_senha

    def get_senha_hash(self) -> str:
        return self.__senha

    def validar(self) -> None:
        if not self._nome or not self._nome.strip():
            raise ValueError("Nome é obrigatório.")
        if "@" not in self._email:
            raise ValueError("E-mail inválido.")
        if len(self.__senha) < 6:
            raise ValueError("Senha deve ter ao menos 6 caracteres.")
        if self._tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Use: {self.TIPOS_VALIDOS}")

    def para_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "email": self._email,
            "tipo": self._tipo,
        }

    def __str__(self) -> str:
        return f"[{self._tipo.upper()}] {self._nome} <{self._email}>"

class Ouvinte(Usuario):
    def __init__(self, nome: str, email: str, senha: str, id: int = None):
        super().__init__(nome, email, senha, tipo="ouvinte", id=id)

    def descricao_plano(self) -> str:
        return "Plano Gratuito — com anúncios, sem downloads."

    def __str__(self) -> str:
        return f"[OUVINTE] {self._nome} <{self._email}>"

class Assinante(Usuario):
    def __init__(self, nome: str, email: str, senha: str, id: int = None):
        super().__init__(nome, email, senha, tipo="assinante", id=id)

    def descricao_plano(self) -> str:
        return "Plano Premium — sem anúncios, downloads ilimitados."

    def __str__(self) -> str:
        return f"[PREMIUM ⭐] {self._nome} <{self._email}>"
