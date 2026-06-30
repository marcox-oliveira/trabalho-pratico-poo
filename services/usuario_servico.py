from models.usuario import Usuario, Ouvinte, Assinante
from repositories.usuario_repo import UsuarioRepositorio

class UsuarioServico:
    def __init__(self):
        self._repo = UsuarioRepositorio()

    def cadastrar(self, nome: str, email: str, senha: str,
                  tipo: str = "ouvinte") -> Usuario:
        if self._repo.buscar_por_email(email):
            raise ValueError(f"Já existe um usuário com o e-mail '{email}'.")

        if tipo == "assinante":
            usuario = Assinante(nome=nome, email=email, senha=senha)
        else:
            usuario = Ouvinte(nome=nome, email=email, senha=senha)
        return self._repo.inserir(usuario)

    def autenticar(self, email: str, senha: str) -> Usuario:
        usuario = self._repo.buscar_por_email(email)
        if not usuario or not usuario.verificar_senha(senha):
            raise ValueError("E-mail ou senha incorretos.")
        return usuario

    def listar(self) -> list:
        return self._repo.listar()

    def buscar_por_id(self, id_: int) -> Usuario:
        usuario = self._repo.buscar_por_id(id_)
        if not usuario:
            raise ValueError(f"Usuário com id={id_} não encontrado.")
        return usuario

    def atualizar_nome(self, id_: int, novo_nome: str) -> None:
        usuario = self.buscar_por_id(id_)
        usuario.nome = novo_nome
        self._repo.atualizar(usuario)

    def promover_para_premium(self, id_: int) -> None:
        usuario = self.buscar_por_id(id_)
        usuario._tipo = "assinante"
        self._repo.atualizar(usuario)

    def excluir(self, id_: int) -> None:
        self.buscar_por_id(id_)
        self._repo.excluir(id_)

    def exibir_plano(self, usuario: Usuario) -> str:
        if hasattr(usuario, "descricao_plano"):
            return usuario.descricao_plano()
        return "Plano desconhecido."
