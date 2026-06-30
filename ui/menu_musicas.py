from services.musica_servico import MusicaServico
from ui.helpers import cabecalho, secao, opcoes, ler_int, ler_bool, pausar

_servico = MusicaServico()

def menu_musicas(usuario_logado):
    while True:
        cabecalho("🎵  CATÁLOGO DE MÚSICAS E PODCASTS")
        opcoes([
            ("1", "Listar todas as mídias"),
            ("2", "Buscar por título"),
            ("3", "Cadastrar música"),
            ("4", "Cadastrar podcast"),
            ("5", "Editar mídia"),
            ("6", "Excluir mídia"),
            ("7", "Reproduzir mídia (demo polimorfismo)"),
            ("0", "Voltar"),
        ])
        op = input("  Opção: ").strip()
        if op == "1":
            _listar()
        elif op == "2":
            _buscar()
        elif op == "3":
            _cadastrar("musica")
        elif op == "4":
            _cadastrar("podcast")
        elif op == "5":
            _editar()
        elif op == "6":
            _excluir()
        elif op == "7":
            _reproduzir()
        elif op == "0":
            break
        else:
            print("  ⚠  Opção inválida.")
        pausar()

def _listar():
    secao("Catálogo de Mídias")
    midias = _servico.listar_midias()
    if not midias:
        print("  Nenhuma mídia cadastrada.")
        return
    for m in midias:
        print(f"  [{m.id:>3}] {m}")

def _buscar():
    secao("Buscar por Título")
    termo = input("  Título (parcial): ").strip()
    resultados = _servico.buscar_por_titulo(termo)
    if not resultados:
        print("  Nenhum resultado encontrado.")
        return
    for m in resultados:
        print(f"  [{m.id:>3}] {m}")

def _cadastrar(tipo: str):
    label = "Música" if tipo == "musica" else "Podcast"
    secao(f"Cadastrar {label}")
    artistas = _servico.listar_artistas()
    if not artistas:
        print("  ⚠  Nenhum artista cadastrado. Cadastre um artista primeiro.")
        return
    print("  Artistas disponíveis:")
    for a in artistas:
        print(f"    [{a.id}] {a.nome}")
    
    titulo = input("  Título: ").strip()
    artista_id = ler_int("  ID do artista: ", minimo=1)
    duracao = ler_int("  Duração (segundos): ", minimo=1)
    genero = input("  Gênero (opcional): ").strip() or None
    albuns = _servico.albuns_do_artista(artista_id)
    album_id = None
    if albuns:
        print("  Álbuns do artista:")
        for alb in albuns:
            print(f"    [{alb.id}] {alb.titulo}")
        resp = input("  ID do álbum (ENTER para nenhum): ").strip()
        if resp:
            album_id = int(resp)

    try:
        if tipo == "musica":
            m = _servico.cadastrar_musica(titulo, duracao, artista_id,
                                          genero, album_id)
        else:
            m = _servico.cadastrar_podcast(titulo, duracao, artista_id,
                                           genero, album_id)
        print(f"  ✅  {label} cadastrada com id={m.id}.")
    except Exception as e:
        print(f"  ⚠  {e}")

def _editar():
    secao("Editar Mídia")
    id_ = ler_int("  ID da mídia: ", minimo=1)
    try:
        m = _servico.buscar_por_id(id_)
        print(f"  Atual: {m}")
    except ValueError as e:
        print(f"  ⚠  {e}")
        return

    titulo = input("  Novo título (ENTER para manter): ").strip() or None
    dur_str = input("  Nova duração em segundos (ENTER para manter): ").strip()
    duracao = int(dur_str) if dur_str else None
    genero = input("  Novo gênero (ENTER para manter): ").strip() or None

    try:
        _servico.atualizar_midia(id_, titulo, duracao, genero)
        print("  ✅  Mídia atualizada.")
    except Exception as e:
        print(f"  ⚠  {e}")

def _excluir():
    secao("Excluir Mídia")
    id_ = ler_int("  ID da mídia: ", minimo=1)
    from ui.helpers import ler_bool
    if not ler_bool("  Confirmar exclusão?"):
        print("  Operação cancelada.")
        return
    try:
        _servico.excluir_midia(id_)
        print("  ✅  Mídia excluída.")
    except Exception as e:
        print(f"  ⚠  {e}")

def _reproduzir():
    secao("Reproduzir Mídia  [demonstração de polimorfismo]")
    id_ = ler_int("  ID da mídia: ", minimo=1)
    try:
        midia = _servico.buscar_por_id(id_)
        resultado = _servico.reproduzir(midia)
        print(f"\n  {resultado}")
        print(f"  Tipo real do objeto: {type(midia).__name__}")
    except ValueError as e:
        print(f"  ⚠  {e}")
