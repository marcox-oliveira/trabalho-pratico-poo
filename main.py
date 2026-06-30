import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.schema import criar_tabelas
from services.usuario_servico import UsuarioServico
from ui.helpers import cabecalho, secao, opcoes, pausar
from ui.menu_usuarios import menu_usuarios
from ui.menu_musicas import menu_musicas
from ui.menu_artistas import menu_artistas
from ui.menu_playlists import menu_playlists

_usuario_servico = UsuarioServico()

def tela_login() -> object:
    """Retorna o usuário autenticado ou encerra o programa."""
    while True:
        cabecalho("🎶  MUSICSTREAM — LOGIN")
        opcoes([
            ("1", "Entrar"),
            ("2", "Cadastrar nova conta"),
            ("0", "Sair"),
        ])
        op = input("  Opção: ").strip()

        if op == "1":
            email = input("  E-mail: ").strip()
            senha = input("  Senha: ").strip()
            try:
                usuario = _usuario_servico.autenticar(email, senha)
                print(f"\n  Bem-vindo(a), {usuario.nome}!")
                print(f"  {_usuario_servico.exibir_plano(usuario)}")
                pausar()
                return usuario
            except ValueError as e:
                print(f"  ⚠  {e}")
                pausar()

        elif op == "2":
            tela_cadastro()

        elif op == "0":
            print("\n  Até logo! 🎵\n")
            sys.exit(0)

        else:
            print("  ⚠  Opção inválida.")
            pausar()

def tela_cadastro():
    secao("Nova Conta")
    nome = input("  Nome: ").strip()
    email = input("  E-mail: ").strip()
    senha = input("  Senha (mín. 6 caracteres): ").strip()
    tipo_str = input("  Tipo [ouvinte / assinante] (ENTER = ouvinte): ").strip().lower()
    tipo = "assinante" if tipo_str == "assinante" else "ouvinte"
    try:
        u = _usuario_servico.cadastrar(nome, email, senha, tipo)
        print(f"  ✅  Conta criada! ID={u.id}  |  {u}")
    except (ValueError, Exception) as e:
        print(f"  ⚠  {e}")
    pausar()

def menu_principal(usuario):
    while True:
        cabecalho(f"🎶  MUSICSTREAM  —  {usuario}")
        opcoes([
            ("1", "🎵  Músicas e Podcasts"),
            ("2", "🎤  Artistas e Álbuns"),
            ("3", "📋  Minhas Playlists"),
            ("4", "👤  Gerenciar Usuários"),
            ("0", "Sair / Trocar conta"),
        ])
        op = input("  Opção: ").strip()

        if op == "1":
            menu_musicas(usuario)
        elif op == "2":
            menu_artistas(usuario)
        elif op == "3":
            menu_playlists(usuario)
        elif op == "4":
            menu_usuarios(usuario)
        elif op == "0":
            break
        else:
            print("  ⚠  Opção inválida.")
            pausar()

def main():
    print("\n  Inicializando banco de dados...")
    try:
        criar_tabelas()
    except Exception as e:
        print(f"\n  ❌  Não foi possível conectar ao banco de dados.\n  {e}")
        print("\n  Verifique as configurações em database/conexao.py")
        sys.exit(1)

    while True:
        usuario = tela_login()
        menu_principal(usuario)

if __name__ == "__main__":
    main()
