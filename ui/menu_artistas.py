from services.musica_servico import MusicaServico
from ui.helpers import cabecalho, secao, opcoes, ler_int, ler_bool, pausar

_servico = MusicaServico()

def menu_artistas(usuario_logado):
    while True:
        cabecalho("🎤  GERENCIAR ARTISTAS")
        opcoes([
            ("1", "Listar artistas"),
            ("2", "Buscar por nome"),
            ("3", "Cadastrar artista"),
            ("4", "Editar artista"),
            ("5", "Excluir artista"),
            ("6", "Listar álbuns do artista"),
            ("7", "Cadastrar álbum"),
            ("0", "Voltar"),
        ])
        op = input("  Opção: ").strip()
        if op == "1":
            _listar()
        elif op == "2":
            _buscar()
        elif op == "3":
            _cadastrar()
        elif op == "4":
            _editar()
        elif op == "5":
            _excluir()
        elif op == "6":
            _albuns()
        elif op == "7":
            _cadastrar_album()
        elif op == "0":
            break
        else:
            print("  ⚠  Opção inválida.")
        pausar()

def _listar():
    secao("Artistas Cadastrados")
    artistas = _servico.listar_artistas()
    if not artistas:
        print("  Nenhum artista cadastrado.")
        return
    for a in artistas:
        print(f"  [{a.id:>3}] {a}")

def _buscar():
    secao("Buscar Artista")
    nome = input("  Nome (parcial): ").strip()
    resultados = _servico.buscar_artistas(nome)
    if not resultados:
        print("  Nenhum artista encontrado.")
        return
    for a in resultados:
        print(f"  [{a.id:>3}] {a}")

def _cadastrar():
    secao("Cadastrar Artista")
    nome = input("  Nome: ").strip()
    genero = input("  Gênero musical (opcional): ").strip() or None
    pais = input("  País (opcional): ").strip() or None
    bio = input("  Bio (opcional): ").strip() or None
    try:
        a = _servico.cadastrar_artista(nome, genero, pais, bio)
        print(f"  ✅  Artista '{a.nome}' cadastrado com id={a.id}.")
    except Exception as e:
        print(f"  ⚠  {e}")

def _editar():
    secao("Editar Artista")
    id_ = ler_int("  ID do artista: ", minimo=1)
    nome = input("  Novo nome (ENTER para manter): ").strip() or None
    genero = input("  Novo gênero (ENTER para manter): ").strip() or None
    pais = input("  Novo país (ENTER para manter): ").strip() or None
    bio = input("  Nova bio (ENTER para manter): ").strip() or None
    try:
        _servico.atualizar_artista(id_, nome, genero, pais, bio)
        print("  ✅  Artista atualizado.")
    except Exception as e:
        print(f"  ⚠  {e}")

def _excluir():
    secao("Excluir Artista")
    id_ = ler_int("  ID do artista: ", minimo=1)
    if not ler_bool("  Confirmar exclusão? (remove álbuns e músicas)"):
        print("  Operação cancelada.")
        return
    try:
        _servico.excluir_artista(id_)
        print("  ✅  Artista excluído.")
    except Exception as e:
        print(f"  ⚠  {e}")

def _albuns():
    secao("Álbuns do Artista")
    id_ = ler_int("  ID do artista: ", minimo=1)
    albuns = _servico.albuns_do_artista(id_)
    if not albuns:
        print("  Nenhum álbum cadastrado para este artista.")
        return
    for alb in albuns:
        print(f"  [{alb.id:>3}] {alb}")

def _cadastrar_album():
    secao("Cadastrar Álbum")
    artistas = _servico.listar_artistas()
    if not artistas:
        print("  ⚠  Nenhum artista cadastrado.")
        return
    for a in artistas:
        print(f"  [{a.id}] {a.nome}")
    artista_id = ler_int("  ID do artista: ", minimo=1)
    titulo = input("  Título do álbum: ").strip()
    ano_str = input("  Ano (opcional): ").strip()
    ano = int(ano_str) if ano_str.isdigit() else None
    try:
        alb = _servico.cadastrar_album(titulo, artista_id, ano)
        print(f"  ✅  Álbum '{alb.titulo}' cadastrado com id={alb.id}.")
    except Exception as e:
        print(f"  ⚠  {e}")
