from database.conexao import obter_conexao, fechar_conexao
from models.usuario import Usuario, Ouvinte, Assinante

class UsuarioRepositorio:
    def _fabricar(self, row) -> Usuario:
        id_, nome, email, senha, tipo = row[0], row[1], row[2], row[3], row[4]
        if tipo == "assinante":
            obj = Assinante.__new__(Assinante)
        else:
            obj = Ouvinte.__new__(Ouvinte)
        obj._id = id_
        obj._nome = nome
        obj._email = email
        obj._Usuario__senha = senha
        obj._tipo = tipo
        return obj

    def inserir(self, usuario: Usuario) -> Usuario:
        usuario.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO usuarios (nome, email, senha, tipo)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (usuario.nome, usuario.email,
                 usuario.get_senha_hash(), usuario.tipo)
            )
            novo_id = cursor.fetchone()[0]
            conexao.commit()
            usuario._id = novo_id
            return usuario
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao inserir usuário: {e}")
        finally:
            fechar_conexao(conexao)

    def listar(self) -> list:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, email, senha, tipo FROM usuarios ORDER BY nome"
            )
            return [self._fabricar(row) for row in cursor.fetchall()]
        finally:
            fechar_conexao(conexao)

    def buscar_por_id(self, id_: int) -> Usuario | None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, email, senha, tipo FROM usuarios WHERE id = %s",
                (id_,)
            )
            row = cursor.fetchone()
            return self._fabricar(row) if row else None
        finally:
            fechar_conexao(conexao)

    def buscar_por_email(self, email: str) -> Usuario | None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, email, senha, tipo FROM usuarios WHERE email = %s",
                (email.strip().lower(),)
            )
            row = cursor.fetchone()
            return self._fabricar(row) if row else None
        finally:
            fechar_conexao(conexao)

    def atualizar(self, usuario: Usuario) -> None:
        usuario.validar()
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute(
                """UPDATE usuarios SET nome=%s, email=%s, senha=%s, tipo=%s
                   WHERE id=%s""",
                (usuario.nome, usuario.email,
                 usuario.get_senha_hash(), usuario.tipo, usuario.id)
            )
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao atualizar usuário: {e}")
        finally:
            fechar_conexao(conexao)

    def excluir(self, id_: int) -> None:
        conexao = None
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_,))
            conexao.commit()
        except Exception as e:
            if conexao:
                conexao.rollback()
            raise RuntimeError(f"Erro ao excluir usuário: {e}")
        finally:
            fechar_conexao(conexao)
