from services.usuario_servico import UsuarioServico
from ui.helpers import cabecalho, secao, opcoes, ler_int, ler_bool, pausar

_servico = UsuarioServico()

def menu_usuarios(usuario_logado):
    while True:
        cabecalho("👤  GERENCIAR USUÁRIOS")
        opcoes([
            ("1", "Listar usuários"),
            ("2", "Buscar por ID"),
            ("3", "Editar nome"),
            ("4", "Promover para Premium"),
            ("5", "Excluir usuário"),
            ("0", "Voltar"),
        ])
        op = input("  Opção: ").strip()
        if op == "1":
            _listar()
        elif op == "2":
            _buscar()
        elif op == "3":
            _editar()
        elif op == "4":
            _promover()
        elif op == "5":
            _excluir()
        elif op == "0":
            break
        else:
            print("  ⚠  Opção inválida.")
        pausar()

def _listar():
    secao("Lista de Usuários")
    usuarios = _servico.listar()
    if not usuarios:
        print("  Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        print(f"  [{u.id:>3}] {u}")

def _buscar():
    secao("Buscar Usuário")
    id_ = ler_int("  ID do usuário: ", minimo=1)
    try:
        u = _servico.buscar_por_id(id_)
        print(f"\n  {u}")
        print(f"  Plano: {_servico.exibir_plano(u)}")
    except ValueError as e:
        print(f"  ⚠  {e}")

def _editar():
    secao("Editar Nome")
    id_ = ler_int("  ID do usuário: ", minimo=1)
    novo_nome = input("  Novo nome: ").strip()
    try:
        _servico.atualizar_nome(id_, novo_nome)
        print("  ✅  Nome atualizado com sucesso.")
    except (ValueError, Exception) as e:
        print(f"  ⚠  {e}")

def _promover():
    secao("Promover para Premium")
    id_ = ler_int("  ID do usuário: ", minimo=1)
    try:
        _servico.promover_para_premium(id_)
        print("  ✅  Usuário promovido para Premium.")
    except Exception as e:
        print(f"  ⚠  {e}")

def _excluir():
    secao("Excluir Usuário")
    id_ = ler_int("  ID do usuário: ", minimo=1)
    if not ler_bool("  Confirmar exclusão?"):
        print("  Operação cancelada.")
        return
    try:
        _servico.excluir(id_)
        print("  ✅  Usuário excluído.")
    except Exception as e:
        print(f"  ⚠  {e}")
